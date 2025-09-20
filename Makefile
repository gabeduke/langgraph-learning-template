# LangGraph Agent Makefile
# ========================

.PHONY: help build run test clean dev prod deploy status logs shell

# Default target
.DEFAULT_GOAL := help

# Variables
APP_NAME := langgraph-agent
DOCKER_IMAGE := dukeman/langgraph:latest
NAMESPACE := langgraph-agent
OPENAI_API_KEY ?= $(shell grep OPENAI_API_KEY .env 2>/dev/null | cut -d '=' -f2)

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)LangGraph Agent - Available Commands$(NC)"
	@echo "=================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development Setup
setup: ## Set up development environment
	@echo "$(BLUE)Setting up development environment...$(NC)"
	@python3 -m venv venv
	@. venv/bin/activate && pip install -r requirements.txt
	@echo "$(GREEN)✅ Virtual environment created and dependencies installed$(NC)"

setup-env: ## Create .env file from template
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "$(YELLOW)⚠️  Please edit .env file with your OpenAI API key$(NC)"; \
	else \
		echo "$(GREEN)✅ .env file already exists$(NC)"; \
	fi

# Docker Operations
build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	@docker build -t $(DOCKER_IMAGE) .
	@echo "$(GREEN)✅ Docker image built: $(DOCKER_IMAGE)$(NC)"

build-no-cache: ## Build Docker image without cache
	@echo "$(BLUE)Building Docker image (no cache)...$(NC)"
	@docker build --no-cache -t $(DOCKER_IMAGE) .
	@echo "$(GREEN)✅ Docker image built: $(DOCKER_IMAGE)$(NC)"

push: ## Push Docker image to registry
	@echo "$(BLUE)Pushing Docker image to registry...$(NC)"
	@docker push $(DOCKER_IMAGE)
	@echo "$(GREEN)✅ Docker image pushed: $(DOCKER_IMAGE)$(NC)"

build-and-push: build push ## Build and push Docker image

# Local Development
run-local: ## Run application locally with Python
	@echo "$(BLUE)Running application locally...$(NC)"
	@if [ -z "$(OPENAI_API_KEY)" ]; then \
		echo "$(RED)❌ OPENAI_API_KEY not set. Please run 'make setup-env' and edit .env file$(NC)"; \
		exit 1; \
	fi
	@. venv/bin/activate && python main.py

run-docker: ## Run with Docker Compose
	@echo "$(BLUE)Running with Docker Compose...$(NC)"
	@docker-compose up

run-docker-bg: ## Run with Docker Compose in background
	@echo "$(BLUE)Running with Docker Compose in background...$(NC)"
	@docker-compose up -d

stop-docker: ## Stop Docker Compose
	@echo "$(BLUE)Stopping Docker Compose...$(NC)"
	@docker-compose down

# Testing
test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	@python test_setup.py
	@echo "$(GREEN)✅ Setup tests passed$(NC)"

test-local: ## Run tests against local application
	@echo "$(BLUE)Running local tests...$(NC)"
	@python test_local.py --target local

test-docker: ## Run tests against Docker application
	@echo "$(BLUE)Running Docker tests...$(NC)"
	@docker-compose up -d
	@sleep 5
	@python test_local.py --target local
	@docker-compose down

test-ingress: ## Run tests against ingress endpoint
	@echo "$(BLUE)Running ingress tests...$(NC)"
	@python test_local.py --target ingress

test-both: ## Run tests against both local and ingress endpoints
	@echo "$(BLUE)Running tests against both local and ingress...$(NC)"
	@python test_local.py --target both

# Learning Plan Tests
test-learning-01: ## Run Learning Plan 1 tests
	@echo "$(BLUE)Running Learning Plan 1 tests...$(NC)"
	@. venv/bin/activate && pytest docs/learning-plans/test_learning_01.py -v

test-learning-02: ## Run Learning Plan 2 tests
	@echo "$(BLUE)Running Learning Plan 2 tests...$(NC)"
	@. venv/bin/activate && pytest docs/learning-plans/test_learning_02.py -v

test-learning-all: ## Run all learning plan tests
	@echo "$(BLUE)Running all learning plan tests...$(NC)"
	@. venv/bin/activate && pytest docs/learning-plans/ -v

test-learning-pytest: ## Run learning plan tests with pytest
	@echo "$(BLUE)Running learning plan tests with pytest...$(NC)"
	@. venv/bin/activate && pytest docs/learning-plans/ -v --tb=short

# Skaffold Operations
dev: ## Start Skaffold development mode
	@echo "$(BLUE)Starting Skaffold development mode...$(NC)"
	@skaffold dev --profile=dev --port-forward

dev-run: ## Run Skaffold once
	@echo "$(BLUE)Running Skaffold once...$(NC)"
	@skaffold run --profile=dev

dev-build: ## Build with Skaffold
	@echo "$(BLUE)Building with Skaffold...$(NC)"
	@skaffold build --profile=dev

dev-deploy: ## Deploy with Skaffold
	@echo "$(BLUE)Deploying with Skaffold...$(NC)"
	@skaffold deploy --profile=dev

dev-delete: ## Delete Skaffold deployment
	@echo "$(BLUE)Deleting Skaffold deployment...$(NC)"
	@skaffold delete --profile=dev

dev-logs: ## Show Skaffold logs
	@echo "$(BLUE)Showing Skaffold logs...$(NC)"
	@skaffold logs --profile=dev

dev-status: ## Show Skaffold status
	@echo "$(BLUE)Showing Skaffold status...$(NC)"
	@kubectl get pods -n $(NAMESPACE)
	@kubectl get services -n $(NAMESPACE)

dev-test: ## Run tests against Skaffold deployment
	@echo "$(BLUE)Running tests against Skaffold deployment...$(NC)"
	@kubectl port-forward service/$(APP_NAME) 8000:8000 -n $(NAMESPACE) &
	@PORT_FORWARD_PID=$$!; \
	sleep 5; \
	python test_local.py --target local; \
	kill $$PORT_FORWARD_PID

dev-test-ingress: ## Run tests against Skaffold deployment via ingress
	@echo "$(BLUE)Running tests against Skaffold deployment via ingress...$(NC)"
	@python test_local.py --target ingress

# Production Operations
prod-build: ## Build production image
	@echo "$(BLUE)Building production image...$(NC)"
	@skaffold build --profile=prod

prod-deploy: ## Deploy to production
	@echo "$(BLUE)Deploying to production...$(NC)"
	@skaffold deploy --profile=prod

# Helm Operations
helm-install: ## Install with Helm
	@echo "$(BLUE)Installing with Helm...$(NC)"
	@if [ -z "$(OPENAI_API_KEY)" ]; then \
		echo "$(RED)❌ OPENAI_API_KEY not set. Please set it as an environment variable$(NC)"; \
		exit 1; \
	fi
	@helm upgrade --install $(APP_NAME) ./helm/$(APP_NAME) \
		--namespace $(NAMESPACE) \
		--create-namespace \
		--set env.OPENAI_API_KEY="$(OPENAI_API_KEY)"

helm-uninstall: ## Uninstall Helm release
	@echo "$(BLUE)Uninstalling Helm release...$(NC)"
	@helm uninstall $(APP_NAME) --namespace $(NAMESPACE)

helm-status: ## Show Helm status
	@echo "$(BLUE)Showing Helm status...$(NC)"
	@helm status $(APP_NAME) --namespace $(NAMESPACE)

# Kubernetes Operations
k8s-status: ## Show Kubernetes status
	@echo "$(BLUE)Kubernetes Status:$(NC)"
	@kubectl get pods -n $(NAMESPACE)
	@kubectl get services -n $(NAMESPACE)
	@kubectl get secrets -n $(NAMESPACE)

k8s-logs: ## Show application logs
	@echo "$(BLUE)Showing application logs...$(NC)"
	@kubectl logs -f deployment/$(APP_NAME) -n $(NAMESPACE)

k8s-shell: ## Get shell access to pod
	@echo "$(BLUE)Getting shell access to pod...$(NC)"
	@kubectl exec -it deployment/$(APP_NAME) -n $(NAMESPACE) -- /bin/bash

k8s-port-forward: ## Port forward to service
	@echo "$(BLUE)Port forwarding to service...$(NC)"
	@kubectl port-forward service/$(APP_NAME) 8000:8000 -n $(NAMESPACE)

# Cleanup Operations
clean: ## Clean up local files
	@echo "$(BLUE)Cleaning up...$(NC)"
	@rm -rf venv/
	@rm -rf __pycache__/
	@rm -rf .pytest_cache/
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "*.pyd" -delete
	@find . -name ".DS_Store" -delete
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

clean-docker: ## Clean up Docker resources
	@echo "$(BLUE)Cleaning up Docker resources...$(NC)"
	@docker-compose down --volumes --remove-orphans
	@docker image prune -f
	@echo "$(GREEN)✅ Docker cleanup complete$(NC)"

clean-k8s: ## Clean up Kubernetes resources
	@echo "$(BLUE)Cleaning up Kubernetes resources...$(NC)"
	@kubectl delete namespace $(NAMESPACE) --ignore-not-found=true
	@echo "$(GREEN)✅ Kubernetes cleanup complete$(NC)"

# Utility Operations
check-deps: ## Check if required tools are installed
	@echo "$(BLUE)Checking dependencies...$(NC)"
	@command -v docker >/dev/null 2>&1 || { echo "$(RED)❌ Docker is not installed$(NC)"; exit 1; }
	@command -v kubectl >/dev/null 2>&1 || { echo "$(RED)❌ kubectl is not installed$(NC)"; exit 1; }
	@command -v helm >/dev/null 2>&1 || { echo "$(RED)❌ Helm is not installed$(NC)"; exit 1; }
	@command -v skaffold >/dev/null 2>&1 || { echo "$(RED)❌ Skaffold is not installed$(NC)"; exit 1; }
	@echo "$(GREEN)✅ All dependencies are installed$(NC)"

lint: ## Run linting
	@echo "$(BLUE)Running linting...$(NC)"
	@. venv/bin/activate && python -m flake8 src/ --max-line-length=100 --ignore=E203,W503
	@echo "$(GREEN)✅ Linting complete$(NC)"

format: ## Format code
	@echo "$(BLUE)Formatting code...$(NC)"
	@. venv/bin/activate && python -m black src/ --line-length=100
	@echo "$(GREEN)✅ Code formatting complete$(NC)"

# Quick start targets
quick-start: setup setup-env build run-docker-bg ## Quick start: setup, build, and run
	@echo "$(GREEN)🎉 Quick start complete!$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "1. Edit .env file with your OpenAI API key"
	@echo "2. Run 'make test-docker' to test the application"
	@echo "3. Visit http://localhost:8000/docs for API documentation"

# Development workflow
dev-workflow: clean setup setup-env build test-docker ## Complete development workflow
	@echo "$(GREEN)🎉 Development workflow complete!$(NC)"
