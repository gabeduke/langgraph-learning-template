#!/usr/bin/env python3
"""
Test script for local development and ingress testing
"""

import requests
import json
import time
import argparse
import os
import subprocess
import sys

def get_ingress_url():
    """Get the ingress URL from Kubernetes or environment variable."""
    # Check environment variable first
    ingress_url = os.getenv('INGRESS_URL')
    if ingress_url:
        return ingress_url.rstrip('/')
    
    # Try to get from Kubernetes
    try:
        result = subprocess.run([
            'kubectl', 'get', 'ingress', 'langgraph-agent', 
            '-n', 'langgraph-agent', 
            '-o', 'jsonpath={.spec.rules[0].host}'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            host = result.stdout.strip()
            # Check if it's a local domain (no dots or ends with .local)
            if '.' not in host or host.endswith('.local'):
                return f"http://{host}"
            else:
                return f"https://{host}"
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    # Default fallback
    return "http://langgraph-agent.local"

def test_health(base_url="http://localhost:8000"):
    """Test health endpoint."""
    print(f"🔍 Testing health endpoint at {base_url}...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_chat(base_url="http://localhost:8000"):
    """Test chat endpoint."""
    print(f"\n🔍 Testing chat endpoint at {base_url}...")
    try:
        payload = {
            "message": "What time is it?",
            "session_id": "test_session"
        }
        response = requests.post(
            f"{base_url}/chat",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat test passed")
            print(f"   Response: {data['response']}")
            print(f"   Tools used: {data['tools_used']}")
            return True
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

def test_chat_modern(base_url="http://localhost:8000"):
    """Test modern chat endpoint."""
    print(f"\n🔍 Testing modern chat endpoint at {base_url}...")
    try:
        payload = {
            "message": "Calculate 15 * 23",
            "session_id": "test_modern"
        }
        response = requests.post(
            f"{base_url}/chat/modern",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Modern chat test passed")
            print(f"   Response: {data['response']}")
            print(f"   Tools used: {data['tools_used']}")
            return True
        else:
            print(f"❌ Modern chat test failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Modern chat test error: {e}")
        return False

def test_streaming(base_url="http://localhost:8000"):
    """Test streaming endpoint."""
    print(f"\n🔍 Testing streaming endpoint at {base_url}...")
    try:
        payload = {
            "message": "Calculate 15 * 23",
            "session_id": "test_stream"
        }
        response = requests.post(
            f"{base_url}/chat/stream",
            json=payload,
            stream=True,
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Streaming test passed")
            print("   Stream chunks:")
            for line in response.iter_lines():
                if line:
                    chunk = line.decode('utf-8')
                    if chunk.startswith('data: '):
                        data = json.loads(chunk[6:])
                        print(f"     {data}")
            return True
        else:
            print(f"❌ Streaming test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Streaming test error: {e}")
        return False

def run_tests_for_target(base_url, target_name):
    """Run all tests for a specific target."""
    print(f"\n🎯 Testing {target_name} at {base_url}")
    print("-" * 50)
    
    tests = [
        test_health,
        test_chat,
        test_chat_modern,
        test_streaming
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test(base_url):
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print(f"\n📊 {target_name} Results: {passed}/{total} passed")
    return passed == total

def main():
    """Run all tests."""
    parser = argparse.ArgumentParser(description='Test LangGraph Agent endpoints')
    parser.add_argument('--target', choices=['local', 'ingress', 'both'], default='local',
                       help='Test target: local (localhost:8000), ingress (K8s ingress), or both')
    parser.add_argument('--ingress-url', help='Override ingress URL (default: auto-detect)')
    parser.add_argument('--wait', type=int, default=5, help='Wait time before starting tests (seconds)')
    
    args = parser.parse_args()
    
    print("🚀 Starting LangGraph Agent Tests")
    print("=" * 50)
    
    # Wait a bit for the service to start
    if args.wait > 0:
        print(f"⏳ Waiting {args.wait} seconds for service to start...")
        time.sleep(args.wait)
    
    all_passed = True
    
    if args.target in ['local', 'both']:
        local_passed = run_tests_for_target("http://localhost:8000", "Local")
        all_passed = all_passed and local_passed
    
    if args.target in ['ingress', 'both']:
        if args.ingress_url:
            ingress_url = args.ingress_url
        else:
            ingress_url = get_ingress_url()
            print(f"🔍 Detected ingress URL: {ingress_url}")
        
        ingress_passed = run_tests_for_target(ingress_url, "Ingress")
        all_passed = all_passed and ingress_passed
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! The agent is working correctly.")
    else:
        print("❌ Some tests failed. Check the logs above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
