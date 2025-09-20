# LangGraph Learning Template

This is a GitHub template repository for learning LangGraph and building production-ready agent systems.

## 🚀 Quick Start

### 1. Create a New Repository
Click the "Use this template" button on GitHub to create your own repository from this template.

### 2. Clone and Setup
```bash
git clone <your-repo-url>
cd <your-repo-name>

# Set up the development environment
make setup
make setup-env

# Edit .env file with your OpenAI API key
# Then test the setup
make test
```

### 3. Start Learning
```bash
# Begin with Learning Plan 1
make test-learning-01

# Or run all learning plans
make test-learning-all
```

## 📚 What You Get

This template provides:

- **Complete LangGraph Implementation**: Both custom and modern patterns
- **5 Comprehensive Learning Plans**: From basic to advanced
- **Production-Ready Setup**: Docker, Kubernetes, Helm charts
- **Comprehensive Testing**: Local, ingress, and learning plan tests
- **MuleSoft Integration Path**: Ready for enterprise integration

## 🎯 Learning Path

1. **[Understand Current Code](docs/learning-plans/01-understand-current-code.md)** - Master the existing implementation
2. **[Interfaces and Extensibility](docs/learning-plans/02-interfaces-and-extensibility.md)** - Deep dive into LangGraph interfaces
3. **[State Stores and Persistence](docs/learning-plans/03-state-stores-and-persistence.md)** - Master state management patterns
4. **[Production Patterns](docs/learning-plans/04-production-patterns.md)** - Learn production-ready patterns
5. **[MuleSoft Integration](docs/learning-plans/05-mulesoft-integration.md)** - Integrate with MuleSoft ecosystems

## 🛠️ Available Commands

```bash
# Development
make setup              # Set up development environment
make run-local          # Run locally
make run-docker         # Run with Docker

# Testing
make test               # Run all tests
make test-local         # Test local endpoints
make test-ingress       # Test ingress endpoints
make test-learning-01   # Learning Plan 1 tests
make test-learning-all  # All learning plan tests

# Deployment
make dev                # Skaffold development
make helm-install       # Helm deployment
make prod-deploy        # Production deployment
```

## 📋 Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Kubernetes cluster (for deployment)
- OpenAI API key

## 🤝 Contributing

This is a learning template. Feel free to:
- Extend the learning plans
- Add new tools and patterns
- Improve the documentation
- Share your implementations

## 📄 License

This template is for educational purposes. Use it to learn and build your own LangGraph applications.

## 🆘 Getting Help

- Check the learning plans for detailed instructions
- Review the test files for implementation examples
- Use the Makefile commands for common tasks
- Ask questions and share your progress

---

**Happy Learning!** 🎉
