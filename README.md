# Chemical Equipment Parameter Visualizer

A hybrid Web and Desktop application for analyzing chemical equipment data with advanced analytics, outlier detection, and health status monitoring.

## 📋 Project Structure

- **`backend/`** - Django REST Framework API with JWT authentication
- **`web-frontend/`** - React + Vite + Chart.js web application
- **`desktop-frontend/`** - PyQt5 + Matplotlib desktop application

📖 **Detailed Documentation:**

- [Web Frontend README](web-frontend/README.md) - Analytics features, health status logic, threshold configuration
- [Desktop Frontend README](desktop-frontend/README.md) - UI features, visualization details, platform notes
- [Backend README](backend/README.md) - Admin panel, user management, database operations

## ⚡ Quick Start

### Prerequisites

- Python 3.8+
- Node.js & npm (for web frontend)

### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
ADMIN_EMAIL=admin@example.com
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

Initialize database:

```bash
python manage.py migrate
python manage.py initadmin
python manage.py runserver
```

Backend runs at: **http://127.0.0.1:8000**

### 2. Web Frontend Setup

```bash
cd web-frontend
npm install
npm run dev
```

Web app runs at: **http://localhost:5173**

### 3. Desktop App Setup

Ensure backend is running first:

```bash
cd desktop-frontend
pip install -r requirements.txt  # PyQt5, matplotlib, requests, numpy
python main.py
```

## 🎯 Core Features

### User Authentication

- **Register**: Create account with username, email, password (8+ characters)
- **Login**: JWT token-based authentication
- **Per-User Data**: Uploads isolated by user account

### Data Analysis

- **CSV Upload**: Drag & drop (web) or file dialog (desktop)
- **Real-Time Processing**: Pandas-based statistical analysis
- **5 Advanced Analytics**:
  1. **Outlier Detection** - IQR method with customizable thresholds
  2. **Type Comparison** - Compare parameters across equipment types
  3. **Correlation Matrix** - Identify parameter relationships
  4. **Enhanced Statistics** - Min/Max/StdDev for all parameters
  5. **Health Status** - Color-coded equipment condition (Normal/Warning/Critical)

### Visualizations

- **Dashboard**: Interactive charts (Chart.js/Matplotlib)
- **Upload History**: Last 5 uploads with click-to-load
- **PDF Reports**: Generate downloadable analysis reports (web only)

## 🩺 Health Status System

Equipment classified into 3 categories:

| Status          | Color  | Criteria                                           |
| --------------- | ------ | -------------------------------------------------- |
| 🟢 **Normal**   | Green  | Parameters within normal range (< 75th percentile) |
| 🟡 **Warning**  | Yellow | Parameters in upper 25% (> 75th percentile)        |
| 🔴 **Critical** | Red    | Parameters are statistical outliers (IQR method)   |

**Thresholds:**

- **Warning**: 75th percentile (top 25% of values)
- **Critical**: IQR outliers (1.5 × IQR beyond Q1/Q3)

**Customization:** See [Web Frontend README](web-frontend/README.md#health-status-threshold-configuration) for details on making thresholds admin-configurable.

## 🔧 Configuration

## 🔧 Configuration

### Environment Variables (`backend/.env`)

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
ADMIN_EMAIL=admin@example.com
```

### Admin Panel Access

Visit: **http://127.0.0.1:8000/admin/**

Use credentials from `.env` file to:

- View all registered users
- Manage uploads
- Monitor system activity

**Change admin password:** Edit `.env` and run `python manage.py initadmin`

## 📊 Analytics Details

### Outlier Detection (IQR Method)

```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

Values outside bounds are flagged as outliers (Critical status).

### Correlation Analysis

Pearson correlation coefficient (-1 to +1) shows relationships:

- **+1**: Perfect positive correlation
- **0**: No correlation
- **-1**: Perfect negative correlation

### Type Comparison

Groups equipment by type and calculates mean Flowrate, Pressure, Temperature for each category.

**For detailed analytics documentation and threshold customization, see:**

- [Web Frontend README - Health Status Configuration](web-frontend/README.md#health-status-threshold-configuration)
- [Desktop Frontend README - Health Status Logic](desktop-frontend/README.md#health-status-logic)

## 🗂️ API Endpoints

| Method | Endpoint             | Auth | Description                      |
| ------ | -------------------- | ---- | -------------------------------- |
| POST   | `/api/register/`     | No   | Create new user account          |
| POST   | `/api/login/`        | No   | Authenticate and get JWT tokens  |
| POST   | `/api/upload/`       | Yes  | Upload CSV file for analysis     |
| GET    | `/api/history/`      | Yes  | Get last 5 uploads (user-scoped) |
| GET    | `/api/uploads/<id>/` | Yes  | Get specific upload details      |
| GET    | `/api/report/<id>/`  | Yes  | Generate PDF report              |

**Authentication:** Include JWT token in header:

```
Authorization: Bearer <access_token>
```

## 🧪 Testing with Sample Data

Sample CSV format (`sample_equipment_data.csv`):

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,45.2,150.5,75.3
Reactor-A1,Reactor,120.0,300.0,185.0
...
```

**Required columns:**

- Equipment Name (string)
- Type (string)
- Flowrate (float)
- Pressure (float)
- Temperature (float)

## 📦 Project Dependencies

### Backend

- Django 6.0.1
- Django REST Framework
- djangorestframework-simplejwt
- pandas
- reportlab
- python-dotenv
- django-cors-headers

### Web Frontend

- React 18
- Vite
- Chart.js
- Axios

### Desktop Frontend

- PyQt5
- Matplotlib
- Requests
- NumPy

## 🔄 Database Management

### Reset Database (Clear all data)

```bash
cd backend
rm db.sqlite3
rm -rf media/uploads/*
python manage.py migrate
python manage.py initadmin
```

### View Uploads

- **Admin Panel**: http://127.0.0.1:8000/admin/ → "Uploaded files"
- **Database**: SQLite browser on `db.sqlite3`

## 🎨 UI Theme

Both web and desktop use a consistent GitHub-inspired dark theme:

| Element      | Hex Color          |
| ------------ | ------------------ |
| Background   | `#0d1117`          |
| Cards/Panels | `#161b22`          |
| Borders      | `#30363d`          |
| Text         | `#c9d1d9`          |
| Accent       | `#58a6ff` (blue)   |
| Success      | `#238636` (green)  |
| Warning      | `#f59e0b` (yellow) |
| Error        | `#ef4444` (red)    |

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**

```bash
lsof -ti:8000 | xargs kill -9  # macOS/Linux
# Or change port: python manage.py runserver 8001
```

**Migration errors:**

```bash
python manage.py migrate --run-syncdb
```

### Web Frontend Issues

**CORS errors:**

- Check `CORS_ALLOWED_ORIGINS` in `backend/.env` includes `http://localhost:5173`
- Restart backend after `.env` changes

**Charts not rendering:**

- Check browser console for errors
- Ensure Chart.js loaded: `npm list chart.js`

### Desktop App Issues

**"Could not connect to server":**

- Ensure backend running on http://127.0.0.1:8000
- Check firewall settings

**PyQt5 import error:**

```bash
pip install --upgrade PyQt5
# macOS: May need system Python or brew install
```

**Matplotlib display issues:**

```bash
# macOS: Set backend
export MPLBACKEND=Qt5Agg
```

## 📝 License

This project is developed as part of the FOSSEE internship screening task.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Version:** 1.0.0  
**Last Updated:** January 2026
