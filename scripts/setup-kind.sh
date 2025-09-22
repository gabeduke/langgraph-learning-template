#!/bin/bash

# Setup script for Kind cluster development
set -e

CLUSTER_NAME="${KIND_CLUSTER_NAME:-langgraph-dev}"

echo "🚀 Setting up Kind cluster for LangGraph Agent with nginx ingress..."

# Check if kind is installed
if ! command -v kind &> /dev/null; then
    echo "❌ Kind is not installed. Please install it first:"
    echo "   brew install kind"
    echo "   or visit: https://kind.sigs.k8s.io/docs/user/quick-start/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install it first."
    exit 1
fi

# Check if cluster already exists
if kind get clusters | grep -q "^$CLUSTER_NAME$"; then
    echo "✅ Kind cluster '$CLUSTER_NAME' already exists"
    echo "🔧 Setting kubectl context..."
    kubectl cluster-info --context kind-$CLUSTER_NAME
else
    # Create kind cluster with ingress configuration
    echo "📦 Creating Kind cluster '$CLUSTER_NAME' with ingress support..."
    cat <<EOF | kind create cluster --name $CLUSTER_NAME --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF

    echo "🌐 Installing nginx ingress controller..."
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
    
    echo "⏳ Waiting for ingress controller to be ready..."
    sleep 10  # Give time for resources to be created
    kubectl wait --namespace ingress-nginx \
      --for=condition=ready pod \
      --selector=app.kubernetes.io/component=controller \
      --timeout=180s

    echo "🔧 Setting kubectl context..."
    kubectl cluster-info --context kind-$CLUSTER_NAME
fi

echo "✅ Kind cluster '$CLUSTER_NAME' is ready with nginx ingress!"
echo ""
echo "📋 Next steps:"
echo "1. Load your Docker images: make kind-load-image"
echo "2. Deploy the application: make kind-deploy"
echo "3. Add to /etc/hosts: echo '127.0.0.1 langgraph.local' | sudo tee -a /etc/hosts"
echo "4. Access the application: http://langgraph.local"
echo ""
echo "🧹 To cleanup: make kind-cleanup"
