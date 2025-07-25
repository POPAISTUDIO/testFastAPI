#!/bin/bash

# FastAPI Image Generation Service Startup Script
# For AWS EC2 Amazon Linux

echo "Starting FastAPI Image Generation Service..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing..."
    sudo yum update -y
    sudo yum install python3 python3-pip -y
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please create one with your Runway API key."
    echo "You can copy env.example to .env and edit it:"
    echo "cp env.example .env"
    echo "Then edit .env and add your RUNWAY_API_KEY"
fi

# Start the application
echo "Starting FastAPI application..."
echo "The API will be available at http://0.0.0.0:8000"
echo "API documentation will be at http://0.0.0.0:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py 