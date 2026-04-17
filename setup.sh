#!/bin/bash

# Setup script for TruthLens AI Scan

echo "🚀 TruthLens AI Scan - Setup Script"
echo "===================================="
echo ""

# Backend setup
echo "1️⃣  Setting up Backend..."
cd backend

# Create virtual environment
echo "   Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "   Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "   Installing Python dependencies..."
pip install -r requirements.txt

# Create placeholder model
echo "   Creating placeholder model..."
python create_model.py

echo "   ✓ Backend setup complete!"
echo ""

# Frontend setup
echo "2️⃣  Setting up Frontend..."
cd ../frontend

# Install dependencies
echo "   Installing Node dependencies..."
npm install

echo "   ✓ Frontend setup complete!"
echo ""

echo "✨ Setup complete!"
echo ""
echo "To start the application:"
echo "1. Backend:  cd backend && source venv/bin/activate && python app.py"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "Then open: http://localhost:3000"
