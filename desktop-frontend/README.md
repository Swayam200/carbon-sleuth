# Desktop Frontend - Chemical Equipment Parameter Visualizer

PyQt5-based desktop application for analyzing and visualizing chemical equipment data with advanced analytics.

## Technology Stack

- **PyQt5**: Desktop GUI framework
- **Matplotlib**: Data visualization library
- **Requests**: HTTP client for API communication
- **Pandas**: Data processing (via backend)
- **NumPy**: Numerical computations for visualizations

## Quick Start

Ensure backend is running first:

```bash
cd ../backend
source venv/bin/activate
python manage.py runserver
```

Then launch desktop app:

```bash
cd desktop-frontend
python main.py
```

## Requirements

Install dependencies:

```bash
pip install PyQt5 matplotlib requests numpy
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## Features Overview

### 1. Login/Register Dialog

**Size:** 350x250px

**Features:**

- Toggle between Login and Register modes
- Email field (register only)
- Password confirmation (register only)
- Form validation before submission
- Green accent buttons for primary actions

**Authentication Flow:**

1. Click "Don't have an account? Register"
2. Fill username, email, password, confirm password
3. Click "Register" button
4. On success, switch to Login mode
5. Enter credentials and click "Login"

### 2. Main Window Layout

**Size:** 1200x800px (default)

**Structure:**

- **Left Sidebar (250px)**: Upload history
- **Main Content Area**: Dashboard and data table tabs
- **Auto-refresh**: History updates every 30 seconds

### 3. Upload Functionality

- Click "Upload CSV" button (green, top-left)
- Select CSV file from file dialog
- Automatic upload and processing
- Status updates in real-time

### 4. Dashboard Tab

#### Basic Statistics Cards (Top Row)

Displays 4 cards with:

- **Total Equipment Count**
- **Average Flowrate** with Min/Max ranges
- **Average Pressure** with Min/Max ranges
- **Average Temperature** with Min/Max ranges

**Styling:**

- Dark background (`#161b22`)
- Rounded corners (8px)
- Border color: `#30363d`

#### Outlier Alert Banner

**When displayed:** When outliers are detected

**Appearance:**

- Red border and background tint
- Warning icon (⚠️)
- Lists up to 5 equipment with outlier parameters
- Shows parameter name, value, and bounds

**Algorithm:** Same as web frontend (IQR method)

#### Main Charts (2 Charts)

1. **Equipment Type Distribution** (Pie Chart)
   - Shows percentage breakdown by type
   - Auto-labels with percentages

2. **Average Parameters** (Bar Chart)
   - 3 bars: Flowrate (blue), Pressure (green), Temperature (red)
   - Y-axis auto-scales to data

#### Advanced Analytics Section (Collapsible)

**Trigger:** Click on "🔬 Advanced Analytics (Click to expand)" group box

**Initial State:** Collapsed (content hidden)

**Contains 4 Subplots:**

##### 1. Type Comparison (Bar Chart)

**Purpose:** Compare parameters across equipment types

**Layout:** Grouped bars (3 per type)

- Blue: Flowrate
- Purple: Pressure
- Red: Temperature

**X-axis:** Equipment types (rotated 45°)

##### 2. Correlation Matrix (Heatmap)

**Purpose:** Show relationships between parameters

**Color Scale:** RdBu_r (Red-Blue reversed)

- Red: Positive correlation
- Blue: Negative correlation
- White: No correlation

**Values:** Displayed in center of each cell (2 decimals)

**Parameters:**

- Flowrate vs Flowrate (always 1.00)
- Flowrate vs Pressure
- Flowrate vs Temperature
- Pressure vs Pressure (always 1.00)
- Pressure vs Temperature
- Temperature vs Temperature (always 1.00)

##### 3. Standard Deviation (Bar Chart)

**Purpose:** Show variability in each parameter

**Bars:**

- Blue: Flowrate StdDev
- Green: Pressure StdDev
- Red: Temperature StdDev

**Interpretation:**

- Higher bar = more variability in that parameter
- Lower bar = consistent values across equipment

##### 4. Health Status Distribution (Pie Chart)

**Purpose:** Overall equipment health overview

**Colors:**

- Green (`#10b981`): Normal status
- Yellow (`#f59e0b`): Warning status
- Red (`#ef4444`): Critical status

**Labels:** Show count and percentage

#### Statistical Summary (Bottom Text)

**Content:**

- Standard deviations for all 3 parameters
- Total equipment types
- Number of outliers detected

### 5. Raw Data Tab

**Table Features:**

- First column: Health status icon
  - ✓ (Green background): Normal
  - ⚠ (Yellow background): Warning
  - ✗ (Red background): Critical
- All CSV columns displayed
- Dark theme styling matching dashboard

**Color-coded Rows:**

- Entire row background matches health status

## Health Status Logic

### Classification Criteria

| Status          | Color  | Hex Code  | Condition                                            |
| --------------- | ------ | --------- | ---------------------------------------------------- |
| 🟢 **Normal**   | Green  | `#10b981` | All parameters below 75th percentile AND no outliers |
| 🟡 **Warning**  | Yellow | `#f59e0b` | Any parameter above 75th percentile BUT no outliers  |
| 🔴 **Critical** | Red    | `#ef4444` | Any parameter is an outlier (IQR method)             |

### Detailed Algorithm

**Step 1: Outlier Detection (IQR Method)**

```python
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

is_outlier = (value < lower_bound) OR (value > upper_bound)
```

**Step 2: Health Status Assignment**

```python
if any_parameter_is_outlier:
    health_status = "critical"
    health_color = "#ef4444"
elif (flowrate > 75th_percentile OR
      pressure > 75th_percentile OR
      temperature > 75th_percentile):
    health_status = "warning"
    health_color = "#f59e0b"
else:
    health_status = "normal"
    health_color = "#10b981"
```

### Threshold Values Explained

#### **Critical Threshold: 1.5 × IQR**

- **Standard:** 1.5 (used by most statistical software)
- **Interpretation:** Values beyond this are statistical anomalies
- **Adjustable:** Change multiplier for stricter (1.0) or more lenient (2.0, 3.0)

**Location in code:** `backend/api/views.py` lines 159-164

#### **Warning Threshold: 75th Percentile**

- **Meaning:** Value is higher than 75% of all equipment
- **Purpose:** Early warning system before reaching critical levels
- **Relative:** Calculated per dataset, not absolute value

**Location in code:** `backend/api/views.py` line 197

**Why 75th percentile?**

- Industry standard for identifying upper quartile
- Balances between catching issues early and avoiding false alarms
- Equipment in top 25% deserves monitoring even if not critical

### Feasibility of Admin-Configurable Thresholds

**Answer: HIGHLY FEASIBLE** ✅

#### Implementation Options:

##### Option 1: Django Settings Model (RECOMMENDED for MVP)

**Effort:** Low (2-3 hours)

**Steps:**

1. Create model:

```python
class AnalyticsSettings(models.Model):
    warning_percentile = models.FloatField(default=0.75,
                                          validators=[MinValueValidator(0.5),
                                                     MaxValueValidator(0.95)])
    outlier_iqr_multiplier = models.FloatField(default=1.5,
                                               validators=[MinValueValidator(0.5),
                                                          MaxValueValidator(3.0)])

    class Meta:
        verbose_name_plural = "Analytics Settings"
```

2. Register in admin panel
3. Query in `FileUploadView`:

```python
settings = AnalyticsSettings.objects.first()
warning_threshold = settings.warning_percentile if settings else 0.75
iqr_multiplier = settings.outlier_iqr_multiplier if settings else 1.5
```

4. Update calculations to use variables instead of hardcoded values

**Pros:**

- Simple to implement
- Uses existing Django admin interface
- No new UI needed
- Can be done in one sprint

**Cons:**

- Changes require backend restart (or use signals to reload)
- Only admin users can access
- Not real-time

##### Option 2: Environment Variables

**Effort:** Very Low (30 minutes)

Add to `backend/.env`:

```env
WARNING_PERCENTILE=0.75
OUTLIER_IQR_MULTIPLIER=1.5
```

Read in code:

```python
import os
warning_threshold = float(os.getenv('WARNING_PERCENTILE', 0.75))
iqr_multiplier = float(os.getenv('OUTLIER_IQR_MULTIPLIER', 1.5))
```

**Pros:**

- Fastest to implement
- No database changes
- DevOps-friendly

**Cons:**

- Requires restart
- Not user-friendly for non-technical admins
- No validation

##### Option 3: REST API + Admin Dashboard (Production-Ready)

**Effort:** High (1-2 days)

**Architecture:**

1. Backend:
   - Model: `AnalyticsSettings`
   - Endpoint: `GET/PUT /api/admin/settings/`
   - Permissions: `IsAdminUser`
   - Cache: Django cache or Redis

2. Frontend (New Admin Page):
   - Settings form with sliders
   - Real-time preview of affected equipment
   - Validation and range constraints
   - Save button

3. Desktop App:
   - Settings dialog accessible from menu
   - Same API integration

**Pros:**

- Best user experience
- Real-time updates (no restart)
- Visual feedback
- Can preview impact before applying
- Both web and desktop admins can use

**Cons:**

- Significant development time
- Requires admin authentication flow
- More testing needed

#### Recommended Implementation Path:

1. **Phase 1 (Now):** Option 2 (Environment Variables)
   - Quick to implement
   - Unblocks testing with different thresholds
   - Good for MVP/demo

2. **Phase 2 (Next Sprint):** Option 1 (Django Admin Model)
   - Better UX than env vars
   - Professional admin interface
   - Validation built-in

3. **Phase 3 (Production):** Option 3 (REST API + Dashboard)
   - Full-featured solution
   - Best for end users
   - Include role-based access control

## API Integration

**Base URL:** `http://127.0.0.1:8000/api/`

**Authentication:** JWT Bearer token

```python
headers = {'Authorization': f'Bearer {token}'}
```

**Used Endpoints:**

- `POST /register/` - User registration
- `POST /login/` - Authentication
- `POST /upload/` - File upload
- `GET /history/` - Upload history

## Color Scheme

Matches web frontend for consistency:

| Element          | Hex Code          |
| ---------------- | ----------------- |
| Background       | `#0d1117`         |
| Cards/GroupBox   | `#161b22`         |
| Borders          | `#30363d`         |
| Text             | `#c9d1d9`         |
| Sidebar          | `#0d1117`         |
| Accent (Buttons) | `#238636` (green) |
| Links            | `#58a6ff` (blue)  |

**Status Colors:**
| Status | Hex Code |
|--------|----------|
| Normal | `#10b981` (green) |
| Warning | `#f59e0b` (yellow) |
| Critical | `#ef4444` (red) |

## Known Issues & Improvements

### Current Limitations:

1. **Window not resizable:** Fixed at 1200x800px
   - **Fix:** Remove `setFixedSize()`, use `resize()` with min/max constraints

2. **Charts not responsive:** Fixed figure sizes
   - **Fix:** Calculate figsize based on window dimensions

3. **No dark mode toggle:** Always dark
   - **Enhancement:** Add settings menu with theme toggle

4. **Limited upload history:** Only last 5 shown
   - **Enhancement:** Add pagination or "Load More" button

### Future Enhancements:

- Export charts as images (PNG/SVG)
- Offline mode with local cache
- Multi-file comparison view
- Custom parameter thresholds per equipment type
- Equipment search/filter in table
- Customizable dashboard layout (drag-drop widgets)

## Troubleshooting

**Issue:** "Could not connect to server"

- **Check:** Backend running on http://127.0.0.1:8000
- **Check:** No firewall blocking port 8000

**Issue:** Charts not displaying

- **Solution:** Ensure matplotlib and numpy installed
- **Check:** `pip list | grep matplotlib`

**Issue:** Login dialog too small on high-DPI displays

- **Solution:** Edit `main.py` line 24: `self.setFixedSize(450, 380)`

**Issue:** Advanced analytics always expanded

- **Solution:** This was fixed - ensure you have latest `main.py`

**Issue:** Table rows not color-coded

- **Solution:** Check backend returns `health_status` and `health_color` fields

## Development Notes

**Main File:** `main.py` (single file application)

**Key Classes:**

- `LoginDialog`: Authentication UI
- `MainWindow`: Main application window
- `FigureCanvas`: Matplotlib chart container

**Data Flow:**

1. User uploads CSV → `upload_file()`
2. Backend processes → Returns JSON with analytics
3. `update_ui(data)` → Updates all visualizations
4. `update_advanced_analytics(summary)` → Renders 4 advanced charts

## Platform-Specific Notes

**macOS:**

- Use system Python or `python3` command
- May need: `pip install --upgrade PyQt5`

**Windows:**

- Ensure Python is in PATH
- Use `python` command (not `python3`)

**Linux:**

- May need: `sudo apt-get install python3-pyqt5`
- Or use virtual environment
