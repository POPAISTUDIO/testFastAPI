#!/bin/bash

# FastAPI Image Generation Service Setup Script
# For AWS EC2 Amazon Linux

set -e  # Exit on any error

echo "=========================================="
echo "FastAPI Image Generation Service Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Run as ec2-user instead."
    exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo yum update -y

# Install Python 3 and pip if not already installed
if ! command -v python3 &> /dev/null; then
    print_status "Installing Python 3..."
    sudo yum install python3 python3-pip -y
else
    print_status "Python 3 is already installed"
fi

# Ensure pip is installed
if ! command -v pip3 &> /dev/null; then
    print_status "Installing python3-pip..."
    sudo yum install python3-pip -y
else
    print_status "pip3 is already installed"
fi

# Install virtual environment if not available
if ! python3 -c "import venv" &> /dev/null; then
    print_status "Installing python3-venv..."
    sudo yum install python3-venv -y
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp env.example .env
    print_warning "Please edit .env file and add your Runway API key:"
    print_warning "  nano .env"
    print_warning "  Add: RUNWAYML_API_SECRET=your_actual_api_key_here"
else
    print_status ".env file already exists"
fi

# Make scripts executable
print_status "Making scripts executable..."
chmod +x start.sh
chmod +x install_service.sh

# Test if the application can start
print_status "Testing application startup..."
if python -c "import fastapi, httpx, pydantic, dotenv, runwayml" 2>/dev/null; then
    print_status "All dependencies are properly installed"
else
    print_error "Some dependencies are missing. Please check the installation."
    exit 1
fi

# Check if port 8000 is available
if netstat -tuln | grep ":8000 " > /dev/null; then
    print_warning "Port 8000 is already in use. You may need to stop other services."
else
    print_status "Port 8000 is available"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Runway API key:"
echo "   nano .env"
echo ""
echo "2. Start the application:"
echo "   ./start.sh"
echo ""
echo "3. Or install as a system service:"
echo "   ./install_service.sh install"
echo "   ./install_service.sh start"
echo ""
echo "4. Test the API:"
echo "   - Open http://localhost:8000/docs for API documentation"
echo "   - Open test_page.html in your browser to test the interface"
echo "   - Run python test_client.py for automated testing"
echo ""
echo "5. Access the API from external clients:"
echo "   - Replace localhost with your EC2 public IP"
echo "   - Make sure port 8000 is open in your security group"
echo ""

# Optional: Check if user wants to start the service now
read -p "Would you like to start the service now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Starting the service..."
    ./start.sh
fi 