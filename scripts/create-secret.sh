#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not found in .env file"
    exit 1
fi

NAMESPACE="langgraph-agent"
SECRET_NAME="langgraph-agent-secrets"

echo "🔑 Creating secret $SECRET_NAME in namespace $NAMESPACE..."

# Create the secret with proper labels that match the Helm chart
kubectl create secret generic $SECRET_NAME \
  --from-literal=openai-api-key="$OPENAI_API_KEY" \
  -n $NAMESPACE \
  --dry-run=client -o yaml | \
kubectl label --local -f - \
  app.kubernetes.io/name=langgraph-agent \
  app.kubernetes.io/instance=langgraph-agent \
  app.kubernetes.io/component=secrets \
  -o yaml | \
kubectl apply -f -

echo "✅ Secret created/updated successfully"
