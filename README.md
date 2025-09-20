# LangGraph Learning Template

A comprehensive LangGraph learning template with 5 structured learning plans, production-ready setup, and MuleSoft integration path. Perfect for learning agent development patterns.

**Docker Registry**: `dukeman/langgraph` on DockerHub

## 🎯 Template Repository

This is a GitHub template repository designed for learning LangGraph patterns. Click "Use this template" to create your own learning repository.

### Template Features
- ✅ **5 Comprehensive Learning Plans** - Structured path from basic to advanced
- ✅ **Production-Ready Setup** - Docker, Kubernetes, Helm charts
- ✅ **Comprehensive Testing** - Unit, integration, and learning validation tests
- ✅ **MuleSoft Integration Path** - Ready for enterprise integration
- ✅ **Clear Documentation** - Step-by-step guides and success criteria

## 🚀 Quick Start

1. **Quick setup and run:**
   ```bash
   make quick-start
   ```

2. **Or step by step:**
   ```bash
   # Set up development environment
   make setup
   
   # Create environment file
   make setup-env
   # Edit .env and add your OpenAI API key
   
   # Run with Docker
   make run-docker
   ```

3. **Deploy to Kubernetes:**
   ```bash
   # Using Skaffold (recommended for development)
   make dev
   
   # Using Helm directly
   export OPENAI_API_KEY=your_key_here
   make helm-install
   ```

## 📁 Project Structure

```
├── src/
│   ├── agent/
│   │   └── core.py          # Core LangGraph agent implementation
│   └── api/
│       ├── models.py        # Pydantic models
│       └── routes.py        # FastAPI routes
├── helm/
│   └── langgraph-agent/     # Helm chart for Kubernetes
├── Makefile                # Main Makefile with all commands
├── main.py                 # Application entry point
├── Dockerfile              # Container definition
├── docker-compose.yml      # Local development
├── skaffold.yaml           # Skaffold configuration
└── requirements.txt        # Python dependencies

## 🔧 Features

### Core Agent (`src/agent/core.py`)
- **State Management**: Uses `MessagesState` for better message handling
- **Tool Integration**: Extensible tool system with basic examples
- **Memory Persistence**: Redis or in-memory checkpointing
- **Streaming Support**: Real-time response streaming
- **Session Management**: Multi-user session support

### Modern Agent (`src/agent/modern.py`)
- **Prebuilt Components**: Uses `create_react_agent` for simplified setup
- **Best Practices**: Follows latest LangGraph patterns
- **Simplified API**: Cleaner interface with modern conventions

### Web API (`src/api/`)
- **FastAPI Framework**: Modern, fast web framework
- **RESTful Endpoints**: `/chat`, `/chat/modern`, `/chat/stream`, `/chat/stream/modern`, `/health`
- **Pydantic Models**: Type-safe request/response models
- **Health Checks**: Kubernetes-ready health endpoints
- **Dual Implementation**: Both custom and modern LangGraph patterns

### Deployment
- **Docker**: Multi-stage build with security best practices
- **Kubernetes**: Full Helm chart with Redis dependency and health checks
- **Scaling**: Horizontal Pod Autoscaler support
- **Security**: Non-root user, proper resource limits
- **Health Checks**: Kubernetes liveness and readiness probes

## 🛠️ LangGraph Patterns Demonstrated

### State Management
```python
# Modern approach using MessagesState
from langgraph.graph.message import MessagesState

# Custom approach with TypedDict
class AgentState(TypedDict):
    messages: Annotated[List, "The conversation messages"]
    user_input: str
    agent_response: str
    session_id: str
    metadata: dict
    tools_used: Annotated[List[str], "List of tools used in this session"]
```

### Tool Integration
The framework includes basic tools that can be extended:

- **Time Tool**: Get current date/time
- **Calculator**: Safe mathematical expressions
- **Echo Tool**: Simple message echoing

### Memory and Persistence
- Redis checkpointing for production
- In-memory fallback for development
- Session-based state management
- Tool usage tracking

## 🔄 API Usage

### Chat Endpoints
```bash
# Custom implementation
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What time is it?", "session_id": "user123"}'

# Modern implementation
curl -X POST "http://localhost:8000/chat/modern" \
  -H "Content-Type: application/json" \
  -d '{"message": "What time is it?", "session_id": "user123"}'
```

### Streaming Endpoints
```bash
# Custom implementation
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{"message": "Calculate 2+2", "session_id": "user123"}'

# Modern implementation
curl -X POST "http://localhost:8000/chat/stream/modern" \
  -H "Content-Type: application/json" \
  -d '{"message": "Calculate 2+2", "session_id": "user123"}'
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 📊 Example Usage

### Local Development
```bash
# Start with Docker Compose
docker-compose up

# Test the API
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What time is it?"}'

# Response
{
  "response": "Current time: 2024-01-15 14:30:25",
  "session_id": "default",
  "tools_used": ["get_current_time"],
  "metadata": {"timestamp": "2024-01-15T14:30:25", "model": "gpt-4o-mini"},
  "timestamp": "2024-01-15T14:30:25"
}
```

### Kubernetes Deployment

#### Using Helm
```bash
# Deploy to your cluster
export OPENAI_API_KEY=your_key_here
./scripts/deploy.sh

# Check deployment
kubectl get pods -n langgraph-agent

# Port forward for testing
kubectl port-forward service/langgraph-agent 8000:8000 -n langgraph-agent
```

#### Using Skaffold (Recommended for Development)
```bash
# Start development mode with hot reload
make dev

# Or run once
make dev-run

# Check status
make dev-status

# Run tests
make dev-test
```

## 🛠️ Available Commands

The project includes a comprehensive Makefile with all necessary commands:

### **Development Commands**
```bash
make help              # Show all available commands
make setup             # Set up development environment
make setup-env         # Create .env file from template
make run-local         # Run application locally with Python
make run-docker        # Run with Docker Compose
make test              # Run all tests
make dev               # Start Skaffold development mode
make dev-test          # Run tests against Skaffold deployment
```

### **Build & Deploy Commands**
```bash
make build             # Build Docker image
make build-no-cache    # Build Docker image without cache
make push              # Push Docker image to registry
make build-and-push    # Build and push Docker image
make helm-install      # Install with Helm
make helm-uninstall    # Uninstall Helm release
make prod-deploy       # Deploy to production
```

### **Utility Commands**
```bash
make clean             # Clean up local files
make clean-docker      # Clean up Docker resources
make clean-k8s         # Clean up Kubernetes resources
make check-deps        # Check if required tools are installed
make lint              # Run code linting
make format            # Format code
```

### **Quick Start Commands**
```bash
make quick-start       # Complete quick start workflow
make dev-workflow      # Complete development workflow
```

## 🔧 Customization

### Adding New Tools
```python
@tool
def your_custom_tool(param: str) -> str:
    """Description of your tool."""
    # Implementation
    return "result"

# Add to the agent in core.py
self.llm_with_tools = self.llm.bind_tools([get_current_time, calculate, echo, your_custom_tool])
```

### Modifying State
```python
class YourCustomState(TypedDict):
    # Add your custom fields
    custom_field: str
    # ... existing fields
```

### Extending Memory
```python
from langgraph.checkpoint.postgres import PostgresSaver

# Use PostgreSQL for production
checkpointer = PostgresSaver.from_conn_string("postgresql://...")
```

## 📚 Learning Plans

This repository includes comprehensive learning plans to master LangGraph:

### 🎯 Learning Path
1. **[Understand Current Code](docs/learning-plans/01-understand-current-code.md)** - Master the existing implementation
2. **[Interfaces and Extensibility](docs/learning-plans/02-interfaces-and-extensibility.md)** - Deep dive into LangGraph interfaces
3. **[State Stores and Persistence](docs/learning-plans/03-state-stores-and-persistence.md)** - Master state management patterns
4. **[Production Patterns](docs/learning-plans/04-production-patterns.md)** - Learn production-ready patterns
5. **[MuleSoft Integration](docs/learning-plans/05-mulesoft-integration.md)** - Integrate with MuleSoft ecosystems

### 🚀 Quick Start Learning
```bash
# Set up learning environment
make setup
make setup-env

# Start with Learning Plan 1
cd docs/learning-plans
python test_learning_01.py
```

Each learning plan includes:
- **Hands-on exercises** with expected outputs
- **Comprehensive test files** for validation
- **Clear success criteria** for completion
- **Additional resources** for deeper understanding

## 📚 Next Steps

1. **Start Learning**: Begin with the learning plans in `docs/learning-plans/`
2. **Test Locally**: Run `docker-compose up` and test the API
3. **Deploy to K8s**: Use the Helm chart in your homelab
4. **Add More Tools**: Extend with domain-specific tools
5. **Add Authentication**: Implement proper security
6. **Add Monitoring**: Implement logging and metrics
7. **Scale**: Test horizontal scaling with HPA

## 🏗️ MuleSoft Integration Path

The learning plans provide a structured path to MuleSoft integration:

1. **Learn LangGraph**: Complete the learning plans to understand patterns
2. **Extend Tools**: Add MuleSoft-specific tools (connectors, flows, etc.)
3. **Custom State**: Add MuleSoft context to the state
4. **API Integration**: Connect to MuleSoft APIs
5. **Deployment**: Adapt for MuleSoft runtime environments

## 🤝 Contributing

This is a learning project for understanding LangGraph patterns. Feel free to extend and modify for your specific use cases.

## 📄 License

This project is for exploration and learning purposes.
# langgraph-learning-template
# langgraph-learning-template
