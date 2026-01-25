# Web Frontend - Chemical Equipment Parameter Visualizer

React-based web application for analyzing and visualizing chemical equipment data with advanced analytics.

## Technology Stack

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Chart.js**: Data visualization library
- **Axios**: HTTP client for API communication

## Quick Start

```bash
npm install
npm run dev
```

Visit: http://localhost:5173/

## Features Overview

### 1. User Authentication

- Register new accounts with email validation
- Login with JWT token-based authentication
- Toggle between login/register modes with a single click

### 2. File Upload

- Drag & drop CSV files or click to browse
- Real-time upload progress indicator
- Automatic data processing and validation

### 3. Dashboard Visualizations

#### Basic Statistics Cards

- **Total Equipment Count**: Number of equipment entries
- **Average Flowrate**: Mean value with min/max ranges
- **Average Pressure**: Mean value with min/max ranges
- **Average Temperature**: Mean value with min/max ranges

#### Main Charts

- **Equipment Type Distribution** (Pie Chart): Breakdown by equipment type
- **Average Parameters** (Bar Chart): Side-by-side comparison of flowrate, pressure, and temperature

### 4. Advanced Analytics (Expandable Section)

#### A. Outlier Detection

**Algorithm:** IQR (Interquartile Range) Method

**Calculation:**

```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR

Outlier if: value < Lower Bound OR value > Upper Bound
```

**Display:**

- Red alert banner when outliers are detected
- Lists up to 5 equipment with outlier parameters
- Shows which parameters (Flowrate, Pressure, Temperature) are outliers with actual values

#### B. Type Comparison Chart (Bar Chart)

**Purpose:** Compare average parameters across different equipment types

**Methodology:**

- Groups equipment by Type field
- Calculates mean Flowrate, Pressure, Temperature for each type
- Displays as grouped bar chart with 3 bars per type

**Use Case:** Identify which equipment types typically operate at higher/lower parameters

#### C. Correlation Heatmap

**Purpose:** Identify relationships between parameters

**Calculation:** Pearson correlation coefficient

```
Values range: -1 to +1
+1: Perfect positive correlation
 0: No correlation
-1: Perfect negative correlation
```

**Color Coding:**

- **Red**: Strong positive correlation (0.6 to 1.0)
- **Yellow**: Moderate correlation (0.3 to 0.6 or -0.3 to -0.6)
- **Blue**: Strong negative correlation (-1.0 to -0.6)
- **Green**: Weak/no correlation (-0.3 to 0.3)

**Interpretation Example:**

- High correlation between Flowrate and Pressure suggests they change together
- Negative correlation suggests inverse relationship

#### D. Health Status Indicators

**Purpose:** Quick visual assessment of equipment condition

**Health Status Classification:**

| Status          | Color  | Hex Code  | Criteria                                                                             |
| --------------- | ------ | --------- | ------------------------------------------------------------------------------------ |
| 🟢 **Normal**   | Green  | `#10b981` | All parameters within normal ranges (below 75th percentile) AND no outliers detected |
| 🟡 **Warning**  | Yellow | `#f59e0b` | One or more parameters in upper 25% (>75th percentile) BUT no outliers               |
| 🔴 **Critical** | Red    | `#ef4444` | One or more parameters flagged as outliers using IQR method                          |

**Detailed Logic:**

```javascript
if (equipment has outlier parameters) {
  status = "Critical" (Red)
} else if (Flowrate > 75th percentile OR
           Pressure > 75th percentile OR
           Temperature > 75th percentile) {
  status = "Warning" (Yellow)
} else {
  status = "Normal" (Green)
}
```

**Warning Threshold Explanation:**

- **75th Percentile**: Means the value is higher than 75% of all equipment
- Equipment in the top 25% (75th-100th percentile) may need monitoring
- This is a relative threshold calculated per dataset

**Why 75th Percentile?**

- Standard statistical practice for identifying high performers/outliers
- Balances sensitivity (catches potential issues) with specificity (avoids false alarms)
- Provides early warning before parameters become critical outliers

#### E. Enhanced Statistics

- **Standard Deviation**: Shows parameter variability
- **Min/Max Values**: Displays full range of each parameter
- **Statistical Summary**: Comprehensive breakdown below charts

## Health Status Threshold Configuration

### Current Implementation

Thresholds are **hardcoded** in the backend (`backend/api/views.py` lines 195-208):

```python
# Warning threshold: 75th percentile
if (row['Flowrate'] > df['Flowrate'].quantile(0.75) or
    row['Pressure'] > df['Pressure'].quantile(0.75) or
    row['Temperature'] > df['Temperature'].quantile(0.75)):
    health_status = 'warning'

# Critical threshold: IQR outlier detection (1.5 × IQR)
```

### Making Thresholds Admin-Configurable

**Feasibility: HIGH** ✅

**Recommended Approaches:**

#### Option 1: Django Admin Settings (Simple) - **RECOMMENDED**

1. Create a `Settings` model in Django:

```python
class AnalyticsSettings(models.Model):
    warning_percentile = models.FloatField(default=0.75)  # 75th percentile
    outlier_multiplier = models.FloatField(default=1.5)   # IQR multiplier
    updated_at = models.DateTimeField(auto_now=True)
```

2. Register in admin panel
3. Query settings in `FileUploadView` before calculations
4. **Pros:** No code changes needed, easy to use
5. **Cons:** Requires backend restart to take effect

#### Option 2: Environment Variables (Moderate)

1. Add to `backend/.env`:

```env
WARNING_PERCENTILE=0.75
OUTLIER_IQR_MULTIPLIER=1.5
```

2. Read in views using `os.getenv()`
3. **Pros:** Can be changed without code deployment
4. **Cons:** Requires server restart

#### Option 3: Admin Dashboard UI (Advanced)

1. Create new React admin dashboard page
2. API endpoint: `PUT /api/settings/`
3. Store in Django cache or database
4. Real-time updates without restart
5. **Pros:** Best UX, instant updates
6. **Cons:** Requires significant development time

**Recommendation for Production:** Option 3 (Admin Dashboard UI) for the best user experience, but start with Option 1 for quick implementation.

### Modifying Thresholds Manually (Current Setup)

To change thresholds, edit `backend/api/views.py`:

1. **Warning Threshold** (line 197):
   - Change `quantile(0.75)` to desired percentile
   - Example: `quantile(0.80)` = 80th percentile (more lenient)
   - Example: `quantile(0.70)` = 70th percentile (more strict)

2. **Critical Threshold** (lines 159-164):
   - Change `1.5 * IQR` multiplier
   - Standard: 1.5 (moderate outlier detection)
   - Strict: 1.0 (more equipment flagged as critical)
   - Lenient: 2.0 or 3.0 (fewer equipment flagged)

**After changes:** Restart backend server for changes to take effect.

## Color Scheme

The web frontend uses a GitHub-inspired dark theme:

| Element                | Color         | Hex Code  |
| ---------------------- | ------------- | --------- |
| Background             | Very Dark     | `#0d1117` |
| Cards/Panels           | Dark Gray     | `#161b22` |
| Borders                | Medium Gray   | `#30363d` |
| Primary Text           | Light Gray    | `#c9d1d9` |
| Accent (Links/Buttons) | Blue          | `#58a6ff` |
| Success/Normal         | Green         | `#10b981` |
| Warning                | Yellow/Orange | `#f59e0b` |
| Error/Critical         | Red           | `#ef4444` |

## API Integration

**Base URL:** `http://127.0.0.1:8000/api/`

**Authentication:** JWT tokens in Authorization header

```javascript
headers: {
  'Authorization': `Bearer ${token}`
}
```

## Build for Production

```bash
npm run build
```

Output in `dist/` directory. Serve with any static file server.

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
