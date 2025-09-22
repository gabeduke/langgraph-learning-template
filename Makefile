# LangGraph Agent Makefile
# ========================

# Variables
APP_NAME := langgraph-agent
DOCKER_IMAGE := dukeman/langgraph:latest
NAMESPACE := langgraph-agent
KIND_CLUSTER_NAME ?= langgraph-dev
OPENAI_API_KEY ?= $(shell grep OPENAI_API_KEY .env 2>/dev/null | cut -d '=' -f2)

# Target configurations
TARGET ?= local
PROFILE ?= dev
PLAN ?= 01
URL ?= 

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

# Core targets
.PHONY: help setup build test deploy status logs shell clean
.PHONY: kind-setup kind-load kind-deploy kind-test kind-cleanup kind-workflow
.PHONY: dev dev-test prod-deploy check-deps lint format quick-start
.PHONY: test-learning test-learning-unit test-learning-api

help: ## Show this help message
	@echo "$(BLUE)LangGraph Agent - Available Commands$(NC)"
	@echo "=================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make setup                    # Setup development environment"
	@echo "  make build                    # Build Docker image"
	@echo "  make test TARGET=local        # Test against local app"
	@echo "  make test TARGET=kind         # Test against Kind cluster"
	@echo "  make deploy PROFILE=kind      # Deploy using kind profile"
	@echo "  make kind-workflow            # Complete Kind setup -> deploy -> test"

# =============================================================================
# Setup & Prerequisites
# =============================================================================

setup: check-deps setup-venv setup-env ## Setup complete development environment
	@echo "$(GREEN)🎉 Development environment ready!$(NC)"

check-deps: ## Check if required tools are installed
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@command -v docker >/dev/null 2>&1 || { echo "$(RED)❌ Docker is not installed$(NC)"; exit 1; }
	@command -v kubectl >/dev/null 2>&1 || { echo "$(RED)❌ kubectl is not installed$(NC)"; exit 1; }
	@command -v helm >/dev/null 2>&1 || { echo "$(RED)❌ Helm is not installed$(NC)"; exit 1; }
	@command -v skaffold >/dev/null 2>&1 || { echo "$(RED)❌ Skaffold is not installed$(NC)"; exit 1; }
	@echo "$(GREEN)✅ All dependencies are installed$(NC)"

setup-venv: ## Set up Python virtual environment
	@echo "$(BLUE)Setting up Python virtual environment...$(NC)"
	@python3 -m venv venv
	@. venv/bin/activate && pip install -r requirements.txt
	@echo "$(GREEN)✅ Virtual environment ready$(NC)"

setup-env: ## Create .env file from template
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "$(YELLOW)⚠️  Please edit .env file with your OpenAI API key$(NC)"; \
	else \
		echo "$(GREEN)✅ .env file already exists$(NC)"; \
	fi

# =============================================================================
# Build Operations
# =============================================================================

build: ## Build Docker image (works for all contexts)
	@echo "$(BLUE)Building Docker image...$(NC)"
	@docker build -t $(DOCKER_IMAGE) .
	@echo "$(GREEN)✅ Docker image built: $(DOCKER_IMAGE)$(NC)"

build-no-cache: ## Build Docker image without cache
	@echo "$(BLUE)Building Docker image (no cache)...$(NC)"
	@docker build --no-cache -t $(DOCKER_IMAGE) .
	@echo "$(GREEN)✅ Docker image built: $(DOCKER_IMAGE)$(NC)"

push: build ## Build and push Docker image to registry
	@echo "$(BLUE)Pushing Docker image to registry...$(NC)"
	@docker push $(DOCKER_IMAGE)
	@echo "$(GREEN)✅ Docker image pushed: $(DOCKER_IMAGE)$(NC)"

# =============================================================================
# Test Operations  
# =============================================================================

test: ## Run tests (use TARGET=local|kind|k8s|url)
	@echo "$(BLUE)Running tests against $(TARGET) target...$(NC)"
	@if [ "$(TARGET)" = "docker" ]; then \
		docker-compose up -d && sleep 5; \
		. venv/bin/activate && python test_suite.py --target local $(if $(URL),--url $(URL)); \
		docker-compose down; \
	else \
		. venv/bin/activate && python test_suite.py --target $(TARGET) $(if $(URL),--url $(URL)); \
	fi

test-setup: ## Run setup tests only
	@echo "$(BLUE)Running setup tests...$(NC)"
	@. venv/bin/activate && python test_suite.py --target $(TARGET) --setup-only

test-learning: ## Run learning plan tests (use PLAN=01|02|all, TARGET=local|kind)
	@echo "$(BLUE)Running learning plan $(PLAN) tests...$(NC)"
	@if [ "$(PLAN)" = "01" ] || [ "$(PLAN)" = "02" ] || [ "$(PLAN)" = "all" ]; then \
		echo "$(YELLOW)🚨 NOTE: Learning Plan tests include DESIGNED FAILURES!$(NC)"; \
		echo "$(YELLOW)   Some tests fail intentionally - implement the exercises to pass.$(NC)"; \
		echo "$(YELLOW)   Read failing tests to understand what to implement.$(NC)"; \
		echo ""; \
	fi
	@. venv/bin/activate && \
	if [ "$(PLAN)" = "all" ]; then \
		pytest docs/learning-plans/ -v --target=$(TARGET); \
	else \
		pytest docs/learning-plans/ -v -m "learning_plan_$(PLAN)" --target=$(TARGET); \
	fi

test-learning-unit: ## Run learning plan unit tests only (no API tests)
	@echo "$(BLUE)Running learning plan unit tests...$(NC)"
	@. venv/bin/activate && pytest docs/learning-plans/ -v -m "not api" --target=$(TARGET)

test-learning-api: ## Run learning plan API tests only
	@echo "$(BLUE)Running learning plan API tests...$(NC)"
	@. venv/bin/activate && pytest docs/learning-plans/ -v -m "api" --target=$(TARGET)

# =============================================================================
# Deploy Operations
# =============================================================================

deploy: ## Deploy using Skaffold (use PROFILE=dev|kind|prod)
	@echo "$(BLUE)Deploying with profile: $(PROFILE)...$(NC)"
	@skaffold run --profile=$(PROFILE)

dev: ## Start development mode with hot reload
	@echo "$(BLUE)Starting development mode...$(NC)"
	@skaffold dev --profile=$(PROFILE) $(if $(filter kind,$(PROFILE)),,--port-forward)

run-local: setup-env ## Run application locally with Python
	@echo "$(BLUE)Running application locally...$(NC)"
	@if [ -z "$(OPENAI_API_KEY)" ]; then \
		echo "$(RED)❌ OPENAI_API_KEY not set. Please edit .env file$(NC)"; \
		exit 1; \
	fi
	@. venv/bin/activate && python main.py

run-docker: ## Run with Docker Compose
	@echo "$(BLUE)Running with Docker Compose...$(NC)"
	@docker-compose up -d

# =============================================================================
# Status & Monitoring
# =============================================================================

status: ## Show application status (works across all contexts)
	@echo "$(BLUE)Application Status:$(NC)"
	@if kubectl get namespace $(NAMESPACE) >/dev/null 2>&1; then \
		echo "$(YELLOW)Kubernetes Status:$(NC)"; \
		kubectl get pods,services,ingress -n $(NAMESPACE); \
	else \
		echo "$(YELLOW)Docker Status:$(NC)"; \
		docker-compose ps 2>/dev/null || echo "No Docker Compose services running"; \
	fi

logs: ## Show application logs
	@echo "$(BLUE)Showing application logs...$(NC)"
	@if kubectl get deployment $(APP_NAME) -n $(NAMESPACE) >/dev/null 2>&1; then \
		kubectl logs -f deployment/$(APP_NAME) -n $(NAMESPACE); \
	else \
		docker-compose logs -f || echo "No Docker Compose logs available"; \
	fi

shell: ## Get shell access to running application
	@echo "$(BLUE)Getting shell access...$(NC)"
	@if kubectl get deployment $(APP_NAME) -n $(NAMESPACE) >/dev/null 2>&1; then \
		kubectl exec -it deployment/$(APP_NAME) -n $(NAMESPACE) -- /bin/bash; \
	else \
		docker-compose exec app /bin/bash 2>/dev/null || echo "No running containers found"; \
	fi

port-forward: ## Port forward to application (when needed)
	@echo "$(BLUE)Port forwarding to application...$(NC)"
	@kubectl port-forward service/$(APP_NAME) 8000:8000 -n $(NAMESPACE)

# =============================================================================
# Kind Cluster Operations
# =============================================================================

kind-setup: ## Setup Kind cluster with nginx ingress
	@echo "$(BLUE)Setting up Kind cluster with nginx ingress...$(NC)"
	@command -v kind >/dev/null 2>&1 || { echo "$(RED)❌ Kind is not installed. Install with: brew install kind$(NC)"; exit 1; }
	@./scripts/setup-kind.sh
	@echo "$(GREEN)✅ Kind cluster setup complete$(NC)"

kind-load: build ## Load Docker image into Kind cluster
	@echo "$(BLUE)Loading Docker image into Kind cluster...$(NC)"
	@kind load docker-image $(DOCKER_IMAGE) --name $(KIND_CLUSTER_NAME)
	@echo "$(GREEN)✅ Docker image loaded into Kind cluster$(NC)"

kind-deploy: ## Deploy to Kind cluster (depends on kind-load)
	@$(MAKE) deploy PROFILE=kind

kind-test: ## Test Kind deployment
	@$(MAKE) test TARGET=kind

kind-cleanup: ## Cleanup Kind cluster
	@echo "$(BLUE)Cleaning up Kind cluster...$(NC)"
	@kind delete cluster --name $(KIND_CLUSTER_NAME)
	@echo "$(GREEN)✅ Kind cluster cleanup complete$(NC)"

kind-workflow: kind-setup kind-load kind-deploy kind-test ## Complete Kind workflow: setup -> load -> deploy -> test
	@echo "$(GREEN)🎉 Kind workflow complete!$(NC)"
	@echo "$(YELLOW)Application is running in Kind cluster with nginx ingress$(NC)"
	@echo "Add to /etc/hosts: echo '127.0.0.1 langgraph.local' | sudo tee -a /etc/hosts"
	@echo "Access via: http://langgraph.local"

# =============================================================================
# Production Operations  
# =============================================================================

prod-deploy: ## Deploy to production
	@$(MAKE) deploy PROFILE=prod

prod-test: ## Test production deployment
	@$(MAKE) test TARGET=k8s

# =============================================================================
# Development Workflows
# =============================================================================

quick-start: setup build run-docker ## Quick start: setup, build, and run locally
	@echo "$(GREEN)🎉 Quick start complete!$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "1. Edit .env file with your OpenAI API key"
	@echo "2. Run 'make test TARGET=docker' to test the application"
	@echo "3. Visit http://localhost:8000/docs for API documentation"

dev-test: ## Run development tests against current deployment
	@$(MAKE) test TARGET=$(if $(filter kind,$(PROFILE)),kind,k8s)

# =============================================================================
# Code Quality
# =============================================================================

lint: setup-venv ## Run linting
	@echo "$(BLUE)Running linting...$(NC)"
	@. venv/bin/activate && python -m flake8 src/ --max-line-length=100 --ignore=E203,W503
	@echo "$(GREEN)✅ Linting complete$(NC)"

format: setup-venv ## Format code
	@echo "$(BLUE)Formatting code...$(NC)"
	@. venv/bin/activate && python -m black src/ --line-length=100
	@echo "$(GREEN)✅ Code formatting complete$(NC)"

# =============================================================================
# Cleanup Operations
# =============================================================================

clean: ## Clean up local files
	@echo "$(BLUE)Cleaning up local files...$(NC)"
	@rm -rf venv/ __pycache__/ .pytest_cache/
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name ".DS_Store" -delete
	@echo "$(GREEN)✅ Local cleanup complete$(NC)"

clean-docker: ## Clean up Docker resources
	@echo "$(BLUE)Cleaning up Docker resources...$(NC)"
	@docker-compose down --volumes --remove-orphans 2>/dev/null || true
	@docker image prune -f
	@echo "$(GREEN)✅ Docker cleanup complete$(NC)"

clean-k8s: ## Clean up Kubernetes resources
	@echo "$(BLUE)Cleaning up Kubernetes resources...$(NC)"
	@kubectl delete namespace $(NAMESPACE) --ignore-not-found=true
	@echo "$(GREEN)✅ Kubernetes cleanup complete$(NC)"

clean-all: clean clean-docker clean-k8s ## Clean up everything
	@echo "$(GREEN)🧹 Complete cleanup finished!$(NC)"
