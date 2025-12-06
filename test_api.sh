#!/bin/bash

echo "🧪 Testing Office Agent API..."
echo ""

echo "1 Health Check:"
curl -s http://localhost:8000/health | jq
echo ""

echo "2 Root Endpoint:"
curl -s http://localhost:8000/ | jq
echo ""

echo "3 Chat Test:"
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! What can you do?",
    "user_id": "test_user"
  }' | jq
echo ""

echo "✅ All tests complete!"