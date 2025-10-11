#!/bin/bash
# Activate virtual environment helper script

echo "🚀 Activating virtual environment..."
source venv/bin/activate

echo "✅ Virtual environment activated!"
echo ""
echo "Python version:"
python --version
echo ""
echo "Installed packages:"
pip list | grep -E "Flask|mediapipe|opencv|psycopg2" | head -10
echo ""
echo "💡 To run the application: python3 app.py"
echo "💡 To deactivate: deactivate"
