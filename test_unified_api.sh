#!/bin/bash

# Test script for Unified API Server
# Tests the new /api/chat endpoint with LangChain agent

echo "🧪 Testing Unified API Server"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base URL
BASE_URL="http://localhost:8000"

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
response=$(curl -s "$BASE_URL/health")
if echo "$response" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
    echo "$response" | jq '.'
else
    echo -e "${RED}✗ Health check failed${NC}"
    echo "$response"
fi
echo ""

# Test 2: Root Endpoint
echo -e "${YELLOW}Test 2: Root Endpoint${NC}"
response=$(curl -s "$BASE_URL/")
if echo "$response" | grep -q "Unified API"; then
    echo -e "${GREEN}✓ Root endpoint passed${NC}"
    echo "$response" | jq '.'
else
    echo -e "${RED}✗ Root endpoint failed${NC}"
    echo "$response"
fi
echo ""

# Test 3: Chat Endpoint (requires real access token)
echo -e "${YELLOW}Test 3: Chat Endpoint${NC}"
echo "Note: This requires a real Google access token from Flutter app"
echo ""

# You need to replace this with a real access token from your Flutter app
# Get it by signing in through Flutter and copying the token
ACCESS_TOKEN="YOUR_ACCESS_TOKEN_HERE"
USER_ID="test_user_123"

if [ "$ACCESS_TOKEN" = "YOUR_ACCESS_TOKEN_HERE" ]; then
    echo -e "${YELLOW}⚠ Skipping chat test - no access token provided${NC}"
    echo "To test chat:"
    echo "1. Sign in through Flutter app"
    echo "2. Get access token from auth_service"
    echo "3. Replace ACCESS_TOKEN in this script"
    echo "4. Run: ./test_unified_api.sh"
else
    echo "Sending test message..."
    response=$(curl -s -X POST "$BASE_URL/api/chat" \
        -H "Content-Type: application/json" \
        -d "{
            \"message\": \"List my latest 5 emails\",
            \"user_id\": \"$USER_ID\",
            \"access_token\": \"$ACCESS_TOKEN\"
        }")
    
    if echo "$response" | grep -q "response"; then
        echo -e "${GREEN}✓ Chat endpoint passed${NC}"
        echo "$response" | jq '.'
    else
        echo -e "${RED}✗ Chat endpoint failed${NC}"
        echo "$response"
    fi
fi
echo ""

# Test 4: Agent Status
echo -e "${YELLOW}Test 4: Agent Status${NC}"
response=$(curl -s "$BASE_URL/api/agent-status/$USER_ID")
echo "$response" | jq '.'
echo ""

echo "=============================="
echo -e "${GREEN}✓ Tests completed${NC}"
echo ""
echo "Next steps:"
echo "1. Make sure Docker containers are running: docker compose up -d"
echo "2. Start the unified API: python api_server_v2.py"
echo "3. Sign in through Flutter app to get access token"
echo "4. Test with real Gmail/Calendar queries"
