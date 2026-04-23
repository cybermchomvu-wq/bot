#!/bin/bash
# Setup script for Football News Website

echo "======================================"
echo "Football News Website - Setup Script"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""
echo "Initializing database..."
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✓ Database initialized')"

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Create an admin user:"
echo "   flask create-admin"
echo ""
echo "3. Start the server:"
echo "   python main.py"
echo ""
echo "4. Open your browser to:"
echo "   http://localhost:5000"
echo ""
echo "======================================"
