#!/bin/bash

# Build script for Kamp Finances executable

echo "🚀 Building Kamp Finances executable..."

# Activate virtual environment
source venv/bin/activate

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/

# Build the executable
echo "🔨 Building executable..."
pyinstaller kamp_finances.spec

# Check if build was successful
if [ -f "dist/KampFinances" ]; then
    echo "✅ Build successful!"
    echo "📁 Executable location: dist/KampFinances"
    echo "💾 Size: $(du -h dist/KampFinances | cut -f1)"
    echo ""
    echo "To run the application:"
    echo "  ./dist/KampFinances"
    echo ""
    echo "To distribute:"
    echo "  Copy the 'dist/KampFinances' file to any Linux system"
else
    echo "❌ Build failed!"
    exit 1
fi 