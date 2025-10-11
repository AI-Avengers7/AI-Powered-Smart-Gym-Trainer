#!/bin/bash
# Start the AI Gym Trainer Application

echo "🚀 Starting AI-Powered Smart Gym Trainer..."
echo "==========================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ .env file created. Please update with your settings."
fi

echo ""
echo "🔧 Environment Check:"
python3 --version
echo "Flask version: $(pip show flask | grep Version)"
echo ""

echo "🌐 Starting Flask Server..."
echo "==========================================="
echo ""
echo "📱 Frontend will be available at:"
echo "   🏠 Home Page:     http://localhost:5000"
echo "   🔐 Login:         http://localhost:5000/auth/login"
echo "   🏋️  Workout:       http://localhost:5000/workout/"
echo "   📊 Analytics:     http://localhost:5000/analytics/"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo "==========================================="
echo ""

# Run the Flask application
python3 app.py
