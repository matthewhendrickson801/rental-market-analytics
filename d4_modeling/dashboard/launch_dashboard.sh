#!/bin/bash

echo "=========================================="
echo "StateofJax Affordable Housing Dashboard"
echo "=========================================="
echo ""
echo "Checking dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Check if required packages are installed
python3 -c "import dash" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Dash not installed. Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "✓ Dependencies installed"
fi

echo ""
echo "Starting dashboard..."
echo "Open your browser to: http://127.0.0.1:8050"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

# Run dashboard
python3 duval_dashboard.py
