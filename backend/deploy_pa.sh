#!/bin/bash

# Configuration
REPO_URL="https://github.com/Swayam200/chemical_equipment_parameter_visualizer.git"
PROJECT_DIR="mysite"
BACKEND_DIR="$PROJECT_DIR/backend"
VENV_DIR="$BACKEND_DIR/venv"

echo "🚀 Starting PythonAnywhere Deployment Automation..."

# 1. Clone Repository if it doesn't exist
if [ ! -d "$PROJECT_DIR" ]; then
    echo "📦 Cloning repository..."
    git clone "$REPO_URL" "$PROJECT_DIR"
else
    echo "🔄 Repository exists. Pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull origin main
    cd ..
fi

# 2. Setup Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# 3. Access Backend & Activate Venv
echo "🔌 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# 4. Install Dependencies
echo "📥 Installing dependencies..."
cd "$BACKEND_DIR"
pip install -r requirements.txt

# 5. Run Migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# 6. Collect Static
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Automatic setup complete!"
echo "👉 Now go to the PythonAnywhere 'Web' tab and configure the WSGI file as described in the guide."
