#!/bin/bash

# Test script for Kamp Finances executable

echo "🧪 Testing Kamp Finances executable..."

# Check if executable exists
if [ ! -f "dist/KampFinances" ]; then
    echo "❌ Executable not found! Run ./build.sh first."
    exit 1
fi

# Check if executable is runnable
if [ ! -x "dist/KampFinances" ]; then
    echo "🔧 Making executable runnable..."
    chmod +x dist/KampFinances
fi

echo "✅ Executable found and runnable"
echo "📁 Location: $(pwd)/dist/KampFinances"
echo "💾 Size: $(du -h dist/KampFinances | cut -f1)"
echo ""
echo "🚀 Starting application (will run in background)..."
echo "   Close the application window when done testing."

# Start the application in background
./dist/KampFinances &

# Wait a moment for the app to start
sleep 2

# Check if the process is running
if pgrep -f "KampFinances" > /dev/null; then
    echo "✅ Application started successfully!"
    echo "   Process ID: $(pgrep -f 'KampFinances')"
    echo ""
    echo "To stop the application:"
    echo "   pkill -f 'KampFinances'"
else
    echo "❌ Application failed to start!"
    exit 1
fi 