#!/bin/bash

echo "🧪 Testing BibTeX Integration..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies with BibTeX support..."
pip install -r requirements.txt

# Test build
echo "🏗️  Testing build with BibTeX..."
pelican content -o test_output -s pelicanconf.py

# Check if bibliography was generated
if [ -f "test_output/index.html" ]; then
    echo "✅ Build successful!"
    
    # Check if bibliography content exists
    if grep -q "publications-list" test_output/index.html; then
        echo "📚 BibTeX integration working!"
    else
        echo "⚠️  BibTeX integration may not be working properly"
    fi
    
    echo "🌐 Test output available at: file://$(pwd)/test_output/index.html"
else
    echo "❌ Build failed!"
fi