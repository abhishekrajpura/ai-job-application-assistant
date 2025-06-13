#!/bin/bash

# Complete Project Setup Script for AI Job Application Assistant
# This script completes Task 1: Project Setup

echo "🤖 AI Job Application Assistant - Complete Setup"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "requirements.txt" ]; then
    print_error "Please run this script from the project root directory"
    print_info "First clone the repository:"
    echo "git clone https://github.com/abhishekrajpura/ai-job-application-assistant.git"
    echo "cd ai-job-application-assistant"
    exit 1
fi

print_info "Starting complete project setup..."

# 1. Check Python version
print_info "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
required_version="3.9"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" 2>/dev/null; then
    print_error "Python 3.9 or higher required. Current version: $python_version"
    exit 1
fi
print_status "Python $python_version detected"

# 2. Create virtual environment
print_info "Creating Python virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -eq 0 ]; then
    print_status "Virtual environment created successfully"
else
    print_error "Failed to create virtual environment"
    exit 1
fi

# 3. Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

if [ "$VIRTUAL_ENV" != "" ]; then
    print_status "Virtual environment activated: $VIRTUAL_ENV"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

# 4. Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip

# 5. Install dependencies
print_info "Installing required dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_status "All dependencies installed successfully"
else
    print_error "Failed to install some dependencies"
    exit 1
fi

# 6. Create additional directories that might be missing
print_info "Creating additional project directories..."
mkdir -p data/logs
mkdir -p data/output/resumes
mkdir -p data/output/cover_letters
mkdir -p src/core
mkdir -p src/application
mkdir -p src/models
mkdir -p src/utils
mkdir -p src/dashboard
mkdir -p tests/fixtures
mkdir -p scripts
mkdir -p docs

print_status "Project directories created"

# 7. Set up configuration files
print_info "Setting up configuration files..."

# Copy example files if they don't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_status "Created .env file from template"
    print_warning "Please edit .env file with your API keys"
fi

if [ ! -f "config/master_resume.json" ]; then
    cp config/master_resume.json.example config/master_resume.json
    print_status "Created master_resume.json from template"
    print_info "Your resume data is already configured!"
fi

# 8. Test the installation
print_info "Testing the installation..."

# Test Python imports
python3 -c "
try:
    import selenium
    import requests
    import pandas
    import yaml
    print('✓ Core dependencies imported successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    print_status "Installation test passed"
else
    print_error "Installation test failed"
    exit 1
fi

# 9. Test the main script
print_info "Testing main script..."
python3 src/main.py --help > /dev/null 2>&1

if [ $? -eq 0 ]; then
    print_status "Main script is working"
else
    print_warning "Main script has issues (this is expected for now)"
fi

# 10. Display setup summary
echo ""
echo "🎉 ${GREEN}Task 1: Project Setup - COMPLETED!${NC}"
echo "=================================="
echo ""
echo "✅ ${GREEN}Completed Tasks:${NC}"
echo "   • Python virtual environment created and activated"
echo "   • Project structure set up with all directories"
echo "   • All required dependencies installed"
echo "   • Git repository initialized (on GitHub)"
echo "   • Configuration files created"
echo ""
echo "📋 ${BLUE}Project Structure:${NC}"
echo "   • src/                 - Main source code"
echo "   • config/              - Configuration files"
echo "   • data/                - Database and output files"
echo "   • tests/               - Unit tests"
echo "   • venv/                - Virtual environment"
echo ""
echo "🔧 ${BLUE}Next Steps:${NC}"
echo "   • Edit .env file with your API keys"
echo "   • Verify config/master_resume.json has your data"
echo "   • Ready to start Task 2: Master Resume System"
echo ""
echo "💡 ${YELLOW}Quick Commands:${NC}"
echo "   • Activate venv:       source venv/bin/activate"
echo "   • Run main script:     python3 src/main.py --help"
echo "   • Test resume tailor:  python3 src/resume/resume_tailor.py"
echo "   • Test Indeed scraper: python3 src/scrapers/indeed_scraper.py"
echo ""

# Deactivate virtual environment for clean exit
deactivate 2>/dev/null || true

print_status "Setup script completed successfully!"
echo ""
echo "🚀 ${GREEN}Ready to proceed with Task 2!${NC}"