"""
Global pytest configuration for LangGraph Agent test suite
Handles target-based testing and service availability checks
"""

import pytest
import requests
import os
import subprocess
from typing import Optional

def pytest_addoption(parser):
    """Add custom command line options for pytest."""
    parser.addoption(
        "--target", 
        action="store", 
        default="local",
        choices=["local", "kind", "k8s"],
        help="Test target: local, kind, or k8s"
    )
    parser.addoption(
        "--skip-service-tests",
        action="store_true",
        default=False,
        help="Skip tests that require the service to be running"
    )
    parser.addoption(
        "--service-url",
        action="store",
        default="http://localhost:8000",
        help="Base URL for service tests"
    )

@pytest.fixture(scope="session")
def test_target(request):
    """Fixture providing the test target."""
    return request.config.getoption("--target")

@pytest.fixture(scope="session") 
def service_url(request):
    """Fixture providing the service URL."""
    return request.config.getoption("--service-url")

@pytest.fixture(scope="session")
def service_available(service_url):
    """Fixture that checks if the service is available."""
    try:
        response = requests.get(f"{service_url}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def pytest_configure(config):
    """Configure pytest with custom markers and behavior."""
    # Register custom markers
    config.addinivalue_line("markers", "unit: Unit tests that don't require external services")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Tests that take a long time to run")

def pytest_collection_modifyitems(config, items):
    """Modify test collection based on configuration."""
    skip_service_tests = config.getoption("--skip-service-tests")
    
    for item in items:
        # Skip API tests if service tests are disabled
        if skip_service_tests and "api" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="Service tests disabled"))
        
        # Skip service-dependent tests if service is not available
        if "skip_if_no_service" in item.keywords:
            item.add_marker(pytest.mark.skipif(
                not is_service_available(config.getoption("--service-url")),
                reason="Service not available"
            ))

def is_service_available(service_url: str) -> bool:
    """Check if the service is available."""
    try:
        response = requests.get(f"{service_url}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

@pytest.fixture
def skip_if_no_kubectl():
    """Skip test if kubectl is not available."""
    try:
        result = subprocess.run(['kubectl', 'version', '--client'], 
                              capture_output=True, timeout=5)
        if result.returncode != 0:
            pytest.skip("kubectl not available")
    except Exception:
        pytest.skip("kubectl not available")

@pytest.fixture
def skip_if_no_kind():
    """Skip test if kind is not available."""
    try:
        result = subprocess.run(['kind', 'version'], 
                              capture_output=True, timeout=5)
        if result.returncode != 0:
            pytest.skip("kind not available")
    except Exception:
        pytest.skip("kind not available")
