#!/usr/bin/env python3
"""
Unified LangGraph Agent Test Suite
Main entry point for testing across different deployment targets
"""

import sys
import os
import argparse
import subprocess
import time

def run_pytest_tests(test_type="unit", additional_args=None):
    """Run pytest tests with the specified test type."""
    cmd = [sys.executable, '-m', 'pytest', 'docs/learning-plans/', '-v']
    
    # Add test type filtering
    if test_type == "unit":
        cmd.extend(['-m', 'not api'])
    elif test_type == "api":
        cmd.extend(['-m', 'api'])
    elif test_type == "all":
        # Run all tests
        pass
    
    if additional_args:
        cmd.extend(additional_args)
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running pytest tests: {e}")
        return False

def run_basic_imports_test():
    """Run basic imports test to verify setup."""
    try:
        # Test basic imports
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from agent.core import LangGraphAgent
        from agent.modern import ModernLangGraphAgent
        print("✅ Agent imports successful")
        
        # Test agent creation
        custom_agent = LangGraphAgent()
        modern_agent = ModernLangGraphAgent()
        print("✅ Agent creation successful")
        
        return True
    except Exception as e:
        print(f"❌ Basic setup test failed: {e}")
        return False

def main():
    """Run the unified test suite."""
    parser = argparse.ArgumentParser(description='LangGraph Agent Unified Test Suite')
    parser.add_argument('--target', choices=['local', 'kind', 'k8s'], default='local',
                       help='Test target: local (python), kind (Kind cluster), k8s (any Kubernetes)')
    parser.add_argument('--setup-only', action='store_true', help='Run setup tests only')
    parser.add_argument('--endpoint-only', action='store_true', help='Run endpoint tests only')
    parser.add_argument('--learning-plans', action='store_true', help='Run learning plan tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--url', help='Custom URL for endpoint tests')
    
    args = parser.parse_args()
    
    print(f"🚀 LangGraph Agent Unified Test Suite")
    print(f"🎯 Target: {args.target}")
    print("=" * 60)
    
    all_passed = True
    
    # Run setup tests (always run unless endpoint-only mode)
    if not args.endpoint_only:
        print("\n📋 Running Basic Setup Tests...")
        setup_passed = run_basic_imports_test()
        all_passed = all_passed and setup_passed
        
        if not setup_passed:
            print("❌ Setup tests failed. Skipping other tests.")
            return False
    
    # Run learning plan unit tests (no API dependencies)
    if not args.endpoint_only and not args.setup_only:
        print("\n🧪 Running Learning Plan Unit Tests...")
        pytest_args = []
        if args.verbose:
            pytest_args.append('--tb=long')
        else:
            pytest_args.append('--tb=short')
        
        # Run unit tests only (no API tests)
        unit_passed = run_pytest_tests("unit", pytest_args)
        all_passed = all_passed and unit_passed
    
    # Run learning plan tests if requested
    if args.learning_plans:
        print("\n📚 Running All Learning Plan Tests...")
        pytest_args = []
        if args.verbose:
            pytest_args.append('--tb=long')
        else:
            pytest_args.append('--tb=short')
        
        learning_passed = run_pytest_tests("all", pytest_args)
        all_passed = all_passed and learning_passed
        
        if learning_passed:
            print("✅ Learning plan tests passed")
        else:
            print("❌ Learning plan tests failed")
    
    print("\n" + "=" * 60)
    if all_passed:
        print(f"🎉 All tests passed for target '{args.target}'!")
        
        print(f"\n📋 Next Steps for '{args.target}':")
        if args.target == "local":
            print("   • Run the application: make run-local")
            print("   • Access API docs: http://localhost:8000/docs")
            print("   • Start learning: make test-learning-01")
        elif args.target == "kind":
            print("   • Access via port forward: make kind-forward")
            print("   • View logs: make kind-logs")
            print("   • Start learning: make test-learning-01")
        elif args.target == "k8s":
            print("   • Check status: make k8s-status")
            print("   • View logs: make k8s-logs")
            print("   • Start learning: make test-learning-01")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
