#!/bin/bash
# Template setup script for new repositories created from this template

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up LangGraph Learning Template${NC}"
echo "=============================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Initializing git repository...${NC}"
    git init
    echo -e "${GREEN}✅ Git repository initialized${NC}"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}⚠️  Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}⚠️  Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Creating .env file...${NC}"
    cp env.example .env
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env file with your OpenAI API key${NC}"
fi

# Run initial tests
echo -e "${YELLOW}⚠️  Running initial tests...${NC}"
make test
echo -e "${GREEN}✅ Setup tests passed${NC}"

# Run learning plan tests
echo -e "${YELLOW}⚠️  Running learning plan tests...${NC}"
make test-learning-01
echo -e "${GREEN}✅ Learning Plan 1 tests passed${NC}"

echo ""
echo -e "${GREEN}🎉 Template setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Edit .env file with your OpenAI API key"
echo "2. Run 'make test-learning-all' to test all learning plans"
echo "3. Start with Learning Plan 1 in docs/learning-plans/"
echo "4. Follow the learning path to master LangGraph"
echo ""
echo -e "${BLUE}Available commands:${NC}"
echo "  make help              # Show all available commands"
echo "  make test-learning-01  # Run Learning Plan 1 tests"
echo "  make test-learning-all # Run all learning plan tests"
echo "  make run-local         # Run application locally"
echo "  make dev               # Start Skaffold development"
echo ""
echo -e "${GREEN}Happy Learning! 🚀${NC}"
