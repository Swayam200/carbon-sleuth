# Backend Administration Guide

This guide covers administrative tasks for managing the Django backend.

## Table of Contents

- [Admin Panel Access](#admin-panel-access)
- [Managing Users](#managing-users)
- [Database Management](#database-management)
- [Environment Configuration](#environment-configuration)
- [🎯 Configuring Health Status Thresholds](#-configuring-health-status-thresholds) ⭐ NEW
- [Troubleshooting](#troubleshooting)
- [Quick Reference Commands](#quick-reference-commands)

---

## Admin Panel Access

### Accessing Django Admin

The Django admin panel provides a web interface to manage users, uploads, and other database objects.

**Steps:**

1. Ensure the backend server is running:

   ```bash
   cd backend
   source venv/bin/activate
   python manage.py runserver
   ```

2. Visit the admin panel:

   ```
   http://127.0.0.1:8000/admin/
   ```

3. Login with admin credentials from your `.env` file:
   - **Username:** Value of `ADMIN_USERNAME` (default: `admin`)
   - **Password:** Value of `ADMIN_PASSWORD` (set in `.env`)

### What You Can Do in Admin Panel

- **View all registered users** (Users section)
- **View all uploads** (Uploaded files section)
- **Create/edit/delete users**
- **View user details** (email, join date, last login, etc.)
- **Change passwords**
- **Manage user permissions** (staff status, superuser status)

---

## Managing Users

### Viewing User List

**Option 1: Django Admin Panel** (Recommended)

1. Visit http://127.0.0.1:8000/admin/
2. Login with admin credentials
3. Click on "Users" under Authentication and Authorization
4. You'll see a complete list of all registered users with:
   - Username
   - Email
   - Staff status
   - Active status
   - Date joined

**Option 2: Django Shell**

```bash
cd backend
source venv/bin/activate
python manage.py shell
```

```python
from django.contrib.auth.models import User

# List all users
users = User.objects.all()
for u in users:
    print(f"ID: {u.id} | Username: {u.username} | Email: {u.email}")
    print(f"   Superuser: {u.is_superuser} | Staff: {u.is_staff}")
    print(f"   Date Joined: {u.date_joined}")
    print(f"   Last Login: {u.last_login}")
    print()

# Count total users
print(f"Total users: {User.objects.count()}")

# Exit shell
exit()
```

**Option 3: Direct SQLite Query**

```bash
cd backend
sqlite3 db.sqlite3
```

```sql
-- View all users
SELECT id, username, email, is_superuser, date_joined FROM auth_user;

-- Count users
SELECT COUNT(*) FROM auth_user;

-- Exit SQLite
.quit
```

### Viewing User Uploads

Each user's uploads are isolated. To view uploads per user:

```python
from django.contrib.auth.models import User
from api.models import UploadedFile

# Get a specific user
user = User.objects.get(username='testuser')

# View their uploads
uploads = UploadedFile.objects.filter(user=user)
for upload in uploads:
    print(f"ID: {upload.id} | File: {upload.file.name}")
    print(f"   Uploaded: {upload.uploaded_at}")
    print(f"   Records: {upload.summary.get('total_count', 0)}")
    print()
```

### Deleting a Specific User

**Via Admin Panel:**

1. Go to http://127.0.0.1:8000/admin/
2. Click "Users"
3. Select the user you want to delete
4. Choose "Delete selected users" from the action dropdown
5. Confirm deletion

**Note:** Deleting a user will also delete all their uploads (cascade delete).

---

## Database Management

### Resetting the Entire Database

If you want to start fresh (delete all users, uploads, and data):

```bash
cd backend

# 1. Delete the database file
rm db.sqlite3

# 2. Delete all uploaded files
rm -rf media/uploads/*

# 3. Recreate database tables
source venv/bin/activate
python manage.py migrate

# 4. Recreate admin user
python manage.py initadmin
```

**Warning:** This will permanently delete:

- All registered users (except admin which will be recreated)
- All uploaded CSV files
- All upload history and statistics

### Resetting Only User Data (Keep Structure)

To delete all users except admin:

```bash
cd backend
source venv/bin/activate
python manage.py shell
```

```python
from django.contrib.auth.models import User
from api.models import UploadedFile

# Delete all uploads
UploadedFile.objects.all().delete()
print("All uploads deleted")

# Delete all non-superuser users
non_admin_users = User.objects.filter(is_superuser=False)
count = non_admin_users.count()
non_admin_users.delete()
print(f"Deleted {count} regular users")

exit()
```

### Backing Up the Database

```bash
cd backend

# Create backup
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)

# List backups
ls -lh db.sqlite3.backup.*
```

### Restoring from Backup

```bash
cd backend

# List available backups
ls -lh db.sqlite3.backup.*

# Restore (replace YYYYMMDD_HHMMSS with your backup timestamp)
cp db.sqlite3.backup.YYYYMMDD_HHMMSS db.sqlite3
```

---

## Environment Configuration

### Updating Admin Credentials

To change the admin password:

1. Edit `backend/.env` file:

   ```env
   ADMIN_PASSWORD=new_secure_password_here
   ```

2. Update the admin user:
   ```bash
   cd backend
   source venv/bin/activate
   python manage.py initadmin
   ```

### Environment Variables

The backend uses the following environment variables (stored in `.env`):

| Variable                 | Description                   | Default                  |
| ------------------------ | ----------------------------- | ------------------------ |
| `DEBUG`                  | Enable debug mode             | `True`                   |
| `SECRET_KEY`             | Django secret key             | (required)               |
| `ALLOWED_HOSTS`          | Comma-separated allowed hosts | `127.0.0.1,localhost`    |
| `CORS_ALLOWED_ORIGINS`   | CORS origins for frontend     | `http://localhost:5173`  |
| `ADMIN_USERNAME`         | Initial admin username        | `admin`                  |
| `ADMIN_PASSWORD`         | Initial admin password        | (required)               |
| `ADMIN_EMAIL`            | Initial admin email           | `admin@example.com`      |
| `WARNING_PERCENTILE`     | Warning threshold percentile  | `0.75` (75th percentile) |
| `OUTLIER_IQR_MULTIPLIER` | IQR multiplier for outliers   | `1.5` (standard)         |

---

## 🎯 Configuring Health Status Thresholds

### Overview

The system classifies equipment into three health statuses:

| Status          | Color  | Criteria                                             |
| --------------- | ------ | ---------------------------------------------------- |
| 🟢 **Normal**   | Green  | Parameters within normal range (< warning threshold) |
| 🟡 **Warning**  | Yellow | Parameters above warning threshold but not outliers  |
| 🔴 **Critical** | Red    | Parameters are statistical outliers                  |

**These thresholds are now configurable!** You can adjust them via the `.env` file without touching any code.

---

### Step-by-Step Tutorial: Changing Thresholds

#### Step 1: Understanding Current Values

Open `backend/.env` and find these lines:

```env
# Analytics Threshold Configuration
WARNING_PERCENTILE=0.75
OUTLIER_IQR_MULTIPLIER=1.5
```

**What they mean:**

- **`WARNING_PERCENTILE=0.75`**
  - Equipment with parameters above 75th percentile = ⚠ Warning
  - Default: Top 25% of equipment get yellow status
  - Range: 0.5 to 0.95

- **`OUTLIER_IQR_MULTIPLIER=1.5`**
  - Multiplier for outlier detection using IQR method
  - Default: Standard statistical outlier detection
  - Range: 0.5 to 3.0

---

#### Step 2: Example Scenarios

**Scenario A: Make Warnings More Strict**

_"I want to catch potential issues earlier - flag equipment in top 30% instead of top 25%"_

**Solution:** Lower the warning percentile

```env
# OLD
WARNING_PERCENTILE=0.75  # Top 25%

# NEW
WARNING_PERCENTILE=0.70  # Top 30%
```

**Result:** More equipment will show ⚠ yellow warning status

---

**Scenario B: Make Warnings More Lenient**

_"Too many false alarms - only flag equipment in top 15%"_

**Solution:** Raise the warning percentile

```env
# OLD
WARNING_PERCENTILE=0.75  # Top 25%

# NEW
WARNING_PERCENTILE=0.85  # Top 15%
```

**Result:** Fewer equipment will show ⚠ yellow warning status

---

**Scenario C: More Sensitive Outlier Detection**

_"Critical alerts are too rare - catch more extreme values"_

**Solution:** Lower the IQR multiplier

```env
# OLD
OUTLIER_IQR_MULTIPLIER=1.5  # Standard

# NEW
OUTLIER_IQR_MULTIPLIER=1.0  # Stricter
```

**Result:** More equipment will show 🔴 red critical status

---

**Scenario D: Less Sensitive Outlier Detection**

_"Too many critical alerts - only flag truly extreme values"_

**Solution:** Raise the IQR multiplier

```env
# OLD
OUTLIER_IQR_MULTIPLIER=1.5  # Standard

# NEW
OUTLIER_IQR_MULTIPLIER=2.0  # More lenient
```

**Result:** Fewer equipment will show 🔴 red critical status

---

#### Step 3: Apply Changes

**Option A: Manual Edit**

1. Open `.env` file in text editor:

   ```bash
   cd backend
   nano .env  # or vim, code, etc.
   ```

2. Modify the values:

   ```env
   WARNING_PERCENTILE=0.80
   OUTLIER_IQR_MULTIPLIER=1.5
   ```

3. Save and close (Ctrl+X for nano)

4. Restart the backend server:
   ```bash
   # Stop current server (Ctrl+C)
   # Then restart:
   python manage.py runserver
   ```

**Option B: Command Line Edit**

```bash
cd backend

# Update warning threshold to 80th percentile
sed -i '' 's/WARNING_PERCENTILE=.*/WARNING_PERCENTILE=0.80/' .env

# Update outlier multiplier to 2.0
sed -i '' 's/OUTLIER_IQR_MULTIPLIER=.*/OUTLIER_IQR_MULTIPLIER=2.0/' .env

# Restart server
python manage.py runserver
```

---

#### Step 4: Verify Changes

1. **Check .env file:**

   ```bash
   cat backend/.env | grep -E "(WARNING_PERCENTILE|OUTLIER_IQR_MULTIPLIER)"
   ```

2. **Upload new CSV** or **view old upload**

3. **Expected results:**
   - New uploads use new thresholds immediately
   - **Old uploads automatically recalculate** when viewed! ✨

---

### Important: Auto-Recalculation Feature ✨

**Unlike typical systems, old uploads are NOT stuck with old thresholds!**

When you change thresholds and view an old upload:

1. System reads current `.env` values
2. Recalculates health status on-the-fly
3. Returns updated colors matching current thresholds

**Example:**

```
Day 1: Upload CSV with WARNING_PERCENTILE=0.75
       → 10 equipment show ⚠ yellow

Day 2: Change .env to WARNING_PERCENTILE=0.85
       Restart server

Day 3: View Day 1 upload
       → System recalculates automatically
       → Now only 6 equipment show ⚠ yellow (using new 85th percentile!)
```

**No manual recalculation needed!** The system is smart. 🧠

---

### Threshold Recommendations by Industry

| Industry                  | Warning Percentile | IQR Multiplier | Reasoning                           |
| ------------------------- | ------------------ | -------------- | ----------------------------------- |
| **Chemical Processing**   | 0.70 (strict)      | 1.0 (strict)   | Safety-critical, catch issues early |
| **General Manufacturing** | 0.75 (standard)    | 1.5 (standard) | Balanced detection                  |
| **Pilot/Experimental**    | 0.85 (lenient)     | 2.0 (lenient)  | Expect variability                  |
| **Quality Control**       | 0.70 (strict)      | 1.0 (strict)   | Tight tolerances required           |
| **Research Labs**         | 0.80 (moderate)    | 2.0 (lenient)  | Exploratory data                    |

---

### Validation & Safety

The system has built-in safety checks:

**Warning Percentile:**

- ✅ Valid: 0.5 to 0.95
- ❌ Invalid: Falls back to 0.75 (default)
- Example: `WARNING_PERCENTILE=1.5` → Uses 0.75 instead

**IQR Multiplier:**

- ✅ Valid: 0.5 to 3.0
- ❌ Invalid: Falls back to 1.5 (default)
- Example: `OUTLIER_IQR_MULTIPLIER=-1` → Uses 1.5 instead

**If .env file is missing these variables:**

- System uses defaults: 0.75 and 1.5
- Everything continues working normally

---

### Testing Your Changes

**Test Plan:**

1. **Before changing thresholds:**

   ```bash
   # Upload a test CSV
   # Note how many warnings/criticals you see
   ```

2. **Change thresholds in .env**

3. **Restart server:**

   ```bash
   cd backend
   source venv/bin/activate
   python manage.py runserver
   ```

4. **View the same upload again:**

   ```bash
   # Click on it in history
   # Colors should be different (if thresholds changed significantly)
   ```

5. **Upload same CSV as new upload:**
   ```bash
   # Upload the CSV again
   # Compare results with old upload
   # Both should now use new thresholds
   ```

---

### Troubleshooting Thresholds

**Problem:** Changed `.env` but seeing same results

**Solutions:**

1. ✅ Restart server (changes require restart)
2. ✅ Check `.env` syntax (no spaces around `=`)
3. ✅ Verify values in range (0.5-0.95 for warning, 0.5-3.0 for outlier)
4. ✅ Check file saved properly: `cat backend/.env`

**Problem:** Too many warnings after change

**Solution:** Increase `WARNING_PERCENTILE` (e.g., 0.75 → 0.80)

**Problem:** Too many critical alerts

**Solution:** Increase `OUTLIER_IQR_MULTIPLIER` (e.g., 1.5 → 2.0)

**Problem:** Missing warnings/criticals

**Solution:**

- Decrease `WARNING_PERCENTILE` (e.g., 0.75 → 0.70)
- Decrease `OUTLIER_IQR_MULTIPLIER` (e.g., 1.5 → 1.0)

---

### Advanced: Understanding the Math

**Warning Threshold (Percentile Method):**

```
If WARNING_PERCENTILE = 0.75:
  - Calculate 75th percentile of all Flowrate values
  - Equipment with Flowrate > 75th percentile = Warning

Example Data: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
  - 75th percentile = 77.5
  - Equipment with Flowrate > 77.5 = Warning
  - That's: 80, 90, 100 (3 out of 10 = top 30%, roughly)
```

**Critical Threshold (IQR Method):**

```
If OUTLIER_IQR_MULTIPLIER = 1.5:
  1. Q1 = 25th percentile
  2. Q3 = 75th percentile
  3. IQR = Q3 - Q1
  4. Lower Bound = Q1 - (1.5 × IQR)
  5. Upper Bound = Q3 + (1.5 × IQR)
  6. Values outside bounds = Critical

Example:
  Q1 = 30, Q3 = 70
  IQR = 70 - 30 = 40
  Lower = 30 - (1.5 × 40) = 30 - 60 = -30
  Upper = 70 + (1.5 × 40) = 70 + 60 = 130

  Equipment with values < -30 or > 130 = Critical
```

---

### Quick Reference: Common Threshold Settings

```env
# Default (Balanced)
WARNING_PERCENTILE=0.75
OUTLIER_IQR_MULTIPLIER=1.5

# Strict (Safety-Critical Applications)
WARNING_PERCENTILE=0.70
OUTLIER_IQR_MULTIPLIER=1.0

# Lenient (Research/Exploratory)
WARNING_PERCENTILE=0.85
OUTLIER_IQR_MULTIPLIER=2.0

# Very Strict (Tight Quality Control)
WARNING_PERCENTILE=0.65
OUTLIER_IQR_MULTIPLIER=1.0

# Very Lenient (Minimize False Alarms)
WARNING_PERCENTILE=0.90
OUTLIER_IQR_MULTIPLIER=2.5
```

---

## Troubleshooting

### "Admin login not working"

- Verify credentials in `.env` file
- Run `python manage.py initadmin` to update admin password
- Check if admin user exists: `python manage.py shell` → `User.objects.filter(username='admin').exists()`

### "Database is locked"

- Stop all running servers: `pkill -f runserver`
- Close any open database connections
- Restart the development server

### "Uploads not showing"

- Uploads are per-user. Make sure you're logged in as the user who uploaded
- Check if files exist: `ls -lh media/uploads/`
- Verify user association: Check admin panel → Uploaded files

### "Migration errors"

If you encounter migration conflicts:

```bash
cd backend
rm db.sqlite3
rm api/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
python manage.py initadmin
```

---

## Quick Reference Commands

```bash
# Start server
python manage.py runserver

# Create admin user
python manage.py initadmin

# Open Django shell
python manage.py shell

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database
rm db.sqlite3 && python manage.py migrate && python manage.py initadmin

# View logs in SQLite
sqlite3 db.sqlite3 "SELECT * FROM api_uploadedfile;"
```

---

## Security Notes

- **Never commit `.env` file** to version control
- **Change default admin password** before deployment
- **Disable DEBUG** in production (`DEBUG=False`)
- **Use strong SECRET_KEY** for production
- **Configure ALLOWED_HOSTS** properly for production
- **Use HTTPS** in production environments
