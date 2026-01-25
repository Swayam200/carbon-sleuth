from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import UploadedFile
from .serializers import UploadedFileSerializer
import pandas as pd
import os
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def get_threshold_settings():
    """
    Get threshold settings from .env with safe fallbacks.
    Returns: (warning_percentile, outlier_iqr_multiplier)
    Defaults to (0.75, 1.5) if not set or invalid.
    """
    try:
        warning = float(os.getenv('WARNING_PERCENTILE', '0.75'))
        # Validate range
        if not (0.5 <= warning <= 0.95):
            warning = 0.75
    except (ValueError, TypeError):
        warning = 0.75
    
    try:
        outlier = float(os.getenv('OUTLIER_IQR_MULTIPLIER', '1.5'))
        # Validate range
        if not (0.5 <= outlier <= 3.0):
            outlier = 1.5
    except (ValueError, TypeError):
        outlier = 1.5
    
    return warning, outlier

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Validation
        if not username or not email or not password:
            return Response(
                {'error': 'All fields are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(password) < 8:
            return Response(
                {'error': 'Password must be at least 8 characters'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)
        
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        # Simple check: did they actually send a file?
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # We only want CSVs here.
        if not file.name.endswith('.csv'):
             return Response({"error": "Only CSV files are allowed"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the file temporarily so we can pass the path to Pandas.
        # This creates a record in the DB and puts the file in /media/uploads
        # Associate upload with the logged-in user
        upload_instance = UploadedFile(file=file, user=request.user)
        upload_instance.save() 

        try:
            # Time to crunch some numbers.
            file_path = upload_instance.file.path
            df = pd.read_csv(file_path)
            
            # Validation: Check for required columns
            required_columns = {'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Missing required columns. Expected: {required_columns}")

            # === ENHANCED ANALYTICS ===
            
            # 1. Basic Statistics with Min/Max/Std Dev
            numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
            stats = {
                "total_count": int(len(df)),
                "avg_flowrate": float(df['Flowrate'].mean()),
                "avg_pressure": float(df['Pressure'].mean()),
                "avg_temperature": float(df['Temperature'].mean()),
                "min_flowrate": float(df['Flowrate'].min()),
                "max_flowrate": float(df['Flowrate'].max()),
                "std_flowrate": float(df['Flowrate'].std()),
                "min_pressure": float(df['Pressure'].min()),
                "max_pressure": float(df['Pressure'].max()),
                "std_pressure": float(df['Pressure'].std()),
                "min_temperature": float(df['Temperature'].min()),
                "max_temperature": float(df['Temperature'].max()),
                "std_temperature": float(df['Temperature'].std()),
                "type_distribution": df['Type'].value_counts().to_dict()
            }
            
            # 2. Type-based Comparison
            type_comparison = {}
            for eq_type in df['Type'].unique():
                type_df = df[df['Type'] == eq_type]
                type_comparison[eq_type] = {
                    "count": int(len(type_df)),
                    "avg_flowrate": float(type_df['Flowrate'].mean()),
                    "avg_pressure": float(type_df['Pressure'].mean()),
                    "avg_temperature": float(type_df['Temperature'].mean())
                }
            stats['type_comparison'] = type_comparison
            
            # 3. Correlation Matrix
            correlation_matrix = df[numeric_cols].corr().to_dict()
            stats['correlation_matrix'] = correlation_matrix
            
            # 4. Outlier Detection (using IQR method)
            # Get configurable thresholds from .env
            warning_percentile, iqr_multiplier = get_threshold_settings()
            
            outliers = []
            for col in numeric_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - iqr_multiplier * IQR  # Configurable
                upper_bound = Q3 + iqr_multiplier * IQR  # Configurable
                
                outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
                for idx in df[outlier_mask].index:
                    equipment_name = df.loc[idx, 'Equipment Name']
                    if equipment_name not in [o['equipment'] for o in outliers]:
                        outliers.append({
                            'equipment': equipment_name,
                            'parameters': []
                        })
                    
                    outlier_entry = next(o for o in outliers if o['equipment'] == equipment_name)
                    outlier_entry['parameters'].append({
                        'parameter': col,
                        'value': float(df.loc[idx, col]),
                        'lower_bound': float(lower_bound),
                        'upper_bound': float(upper_bound)
                    })
            
            stats['outliers'] = outliers
            
            # 5. Health Status for each equipment
            data_json = df.to_dict(orient='records')
            for i, row in enumerate(data_json):
                equipment_name = row['Equipment Name']
                
                # Check if equipment has outliers
                is_outlier = any(o['equipment'] == equipment_name for o in outliers)
                
                # Simple health status based on parameter ranges
                # Critical: Any parameter is an outlier
                # Warning: Parameters above warning_percentile (configurable)
                # Normal: Everything else
                if is_outlier:
                    health_status = 'critical'
                    health_color = '#ef4444'  # red
                elif (row['Flowrate'] > df['Flowrate'].quantile(warning_percentile) or 
                      row['Pressure'] > df['Pressure'].quantile(warning_percentile) or 
                      row['Temperature'] > df['Temperature'].quantile(warning_percentile)):
                    health_status = 'warning'
                    health_color = '#f59e0b'  # yellow
                else:
                    health_status = 'normal'
                    health_color = '#10b981'  # green
                
                data_json[i]['health_status'] = health_status
                data_json[i]['health_color'] = health_color

            # We also send back the raw data so the frontend can display the table.
            # .to_dict('records') gives us a nice list of JSON objects.

            # Save the results back to the instance so we don't have to re-process it later.
            upload_instance.summary = stats
            upload_instance.processed_data = data_json
            upload_instance.save()

            # Housekeeping: We only want to keep the last 5 uploads PER USER to avoid cluttering the server.
            # If we represent a real production app, we might archive these instead or use S3 with lifecycle policies.
            user_files = UploadedFile.objects.filter(user=request.user)
            if user_files.count() > 5:
                # Get the IDs of the 5 newest files for this user, and delete anything that's NOT in that list.
                ids_to_keep = user_files[:5].values_list('id', flat=True)
                UploadedFile.objects.filter(user=request.user).exclude(id__in=ids_to_keep).delete()

            serializer = UploadedFileSerializer(upload_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # If anything goes wrong (bad CSV format, permissions, etc), cleanup the database record.
            upload_instance.delete()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HistoryView(generics.ListAPIView):
    serializer_class = UploadedFileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return only the current user's uploads
        return UploadedFile.objects.filter(user=self.request.user)[:5]

class PDFReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            # Ensure user can only access their own reports
            instance = UploadedFile.objects.get(pk=pk, user=request.user)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{pk}.pdf"'

            p = canvas.Canvas(response)
            p.drawString(100, 800, f"Equipment Data Analysis Report - ID {pk}")
            p.drawString(100, 780, f"Uploaded At: {instance.uploaded_at}")
            
            stats = instance.summary
            p.drawString(100, 750, "Summary Statistics:")
            p.drawString(120, 730, f"Total Equipment Count: {stats.get('total_count', 0)}")
            p.drawString(120, 715, f"Average Flowrate: {stats.get('avg_flowrate', 0):.2f}")
            p.drawString(120, 700, f"Average Pressure: {stats.get('avg_pressure', 0):.2f}")
            p.drawString(120, 685, f"Average Temperature: {stats.get('avg_temperature', 0):.2f}")

            p.drawString(100, 650, "Type Distribution:")
            y = 635
            for k, v in stats.get('type_distribution', {}).items():
                p.drawString(120, y, f"{k}: {v}")
                y -= 15
            
            p.showPage()
            p.save()
            return response
        except UploadedFile.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
