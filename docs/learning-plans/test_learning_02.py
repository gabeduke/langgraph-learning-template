#!/usr/bin/env python3
"""
🚨 IMPORTANT: THESE TESTS ARE DESIGNED TO FAIL! 🚨

Test file for Learning Plan 2: Interfaces and Extensibility
═══════════════════════════════════════════════════════════

❌ EXPECTED BEHAVIOR: All tests will FAIL until you implement the exercises
✅ THIS IS INTENTIONAL: Failures guide your learning journey

🎯 Test-Driven Learning Flow:
1. 🔴 Run tests - they WILL fail (this is good!)
2. 📖 Read the failing test to understand what to implement  
3. 💡 Check the error message for implementation guidance
4. 🔧 Implement the required functionality in the specified file
5. 🔄 Run tests again - they should now pass
6. ➡️  Move to next failing test and repeat

🛠️ Quick Start:
   make test-learning PLAN=02    # See the failing tests
   # Read the first failure, implement the solution
   # Re-run until all tests pass!

📁 Implementation Files: src/agent/custom_nodes.py, src/agent/custom_state.py, etc.
"""

import pytest
import asyncio
from typing import Dict, Any, List
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from agent.core import LangGraphAgent
from agent.modern import ModernLangGraphAgent

# Test markers for different environments
pytestmark = pytest.mark.learning_plan_02

class TestCustomNodes:
    """Test custom node implementations - THESE WILL FAIL UNTIL YOU IMPLEMENT THEM."""
    
    def test_multi_operation_node(self):
        """
        🧪 Exercise 1.1: Create a node that performs multiple operations
        
        You need to create a custom node class that:
        1. Inherits from a proper base class
        2. Performs multiple operations in sequence
        3. Handles intermediate results
        4. Returns a structured response
        
        📁 Implement in: src/agent/custom_nodes.py
        """
        from agent.custom_nodes import MultiOperationNode
        
        node = MultiOperationNode()
        
        # Test the node can handle multiple operations
        input_data = {
            "operations": ["validate_input", "process_data", "format_output"],
            "data": {"value": 42, "type": "number"}
        }
        
        result = node.execute(input_data)
        
        assert result["success"] == True
        assert "validation_result" in result
        assert "processed_data" in result  
        assert "formatted_output" in result
        assert result["operations_completed"] == 3
    
    def test_stateful_node(self):
        """
        🧪 Exercise 1.2: Create a node with internal state
        
        You need to create a stateful node that:
        1. Maintains internal state between calls
        2. Updates state based on inputs
        3. Provides state introspection
        4. Handles state reset
        
        📁 Implement in: src/agent/custom_nodes.py
        """
        from agent.custom_nodes import StatefulNode
        
        node = StatefulNode()
        
        # Test initial state
        assert node.get_state() == {}
        
        # Test state updates
        node.update_state({"counter": 1, "last_input": "test"})
        state = node.get_state()
        assert state["counter"] == 1
        assert state["last_input"] == "test"
        
        # Test state persistence across calls
        node.process({"action": "increment"})
        state = node.get_state()
        assert state["counter"] == 2
        
        # Test state reset
        node.reset_state()
        assert node.get_state() == {}
    
    def test_retry_node(self):
        """
        🧪 Exercise 1.3: Create a node with retry logic
        
        You need to create a retry node that:
        1. Attempts operations with configurable retries
        2. Implements exponential backoff
        3. Handles different failure types
        4. Provides retry statistics
        
        📁 Implement in: src/agent/custom_nodes.py
        """
        from agent.custom_nodes import RetryNode
        
        node = RetryNode(max_retries=3, base_delay=0.1)
        
        # Test successful operation (no retries needed)
        result = node.execute({"operation": "success", "data": "test"})
        assert result["success"] == True
        assert result["retry_count"] == 0
        
        # Test operation that fails initially but succeeds on retry
        result = node.execute({"operation": "fail_twice", "data": "test"})
        assert result["success"] == True
        assert result["retry_count"] == 2
        
        # Test operation that exhausts retries
        result = node.execute({"operation": "always_fail", "data": "test"})
        assert result["success"] == False
        assert result["retry_count"] == 3
        assert "final_error" in result
    
    def test_batch_processing_node(self):
        """
        🧪 Exercise 1.4: Create a node that processes batches
        
        You need to create a batch processing node that:
        1. Handles multiple items efficiently
        2. Implements parallel processing
        3. Provides progress tracking
        4. Handles partial failures gracefully
        
        📁 Implement in: src/agent/custom_nodes.py
        """
        from agent.custom_nodes import BatchProcessingNode
        
        node = BatchProcessingNode(batch_size=3, parallel=True)
        
        # Test batch processing
        items = [{"id": i, "value": i * 2} for i in range(10)]
        result = node.process_batch(items)
        
        assert result["total_items"] == 10
        assert result["successful_items"] == 10
        assert result["failed_items"] == 0
        assert len(result["results"]) == 10
        assert result["processing_time"] > 0

class TestAdvancedStateManagement:
    """Test advanced state management - THESE WILL FAIL UNTIL YOU IMPLEMENT THEM."""
    
    def test_custom_state_validation(self):
        """
        🧪 Exercise 2.1: Create state class with validation
        
        You need to create a custom state class that:
        1. Inherits from MessagesState or TypedDict
        2. Implements field validation
        3. Provides clear error messages
        4. Supports nested validation
        
        📁 Implement in: src/agent/custom_state.py
        """
        from agent.custom_state import ValidatedState
        
        # Test valid state creation
        state = ValidatedState(
            messages=[],
            user_id="user123",
            session_data={"preference": "dark_mode"},
            metadata={"version": "1.0"}
        )
        
        assert state.is_valid()
        assert state.user_id == "user123"
        
        # Test validation errors
        with pytest.raises(ValueError, match="user_id must be provided"):
            ValidatedState(messages=[], user_id="")
            
        with pytest.raises(ValueError, match="Invalid session_data format"):
            ValidatedState(messages=[], user_id="user123", session_data="invalid")
    
    def test_state_transitions(self):
        """
        🧪 Exercise 2.2: Implement state transitions with business logic
        
        You need to create a state manager that:
        1. Defines valid state transitions
        2. Implements transition rules
        3. Validates state changes
        4. Provides transition history
        
        📁 Implement in: src/agent/state_manager.py
        """
        from agent.state_manager import StateTransitionManager
        
        manager = StateTransitionManager()
        
        # Test valid transitions
        manager.transition_to("authenticated", {"user_id": "user123"})
        assert manager.current_state == "authenticated"
        
        manager.transition_to("processing", {"task_id": "task456"})
        assert manager.current_state == "processing"
        
        # Test invalid transitions
        with pytest.raises(ValueError, match="Invalid transition"):
            manager.transition_to("completed", {})  # Missing required data
            
        # Test transition history
        history = manager.get_transition_history()
        assert len(history) >= 2
        assert history[-1]["to_state"] == "processing"
    
    def test_state_persistence(self):
        """
        🧪 Exercise 2.3: Add state persistence and recovery
        
        You need to create a persistent state manager that:
        1. Saves state to storage
        2. Recovers state on restart
        3. Handles corruption gracefully
        4. Implements versioning
        
        📁 Implement in: src/agent/persistent_state.py
        """
        from agent.persistent_state import PersistentStateManager
        
        # Test state persistence
        manager1 = PersistentStateManager("test_session")
        manager1.update_state({"counter": 5, "data": "test"})
        manager1.save()
        
        # Test state recovery
        manager2 = PersistentStateManager("test_session")
        manager2.load()
        
        assert manager2.get_state()["counter"] == 5
        assert manager2.get_state()["data"] == "test"
        
        # Test versioning
        assert manager2.get_version() > 0
        
        # Cleanup
        manager2.clear()
    
    def test_state_analytics(self):
        """
        🧪 Exercise 2.4: Add state analytics and monitoring
        
        You need to create a state analytics system that:
        1. Tracks state changes over time
        2. Provides usage statistics
        3. Identifies patterns and anomalies
        4. Generates performance insights
        
        📁 Implement in: src/agent/state_analytics.py
        """
        from agent.state_analytics import StateAnalytics
        
        analytics = StateAnalytics()
        
        # Simulate state changes
        for i in range(10):
            analytics.track_state_change(
                f"state_{i % 3}", 
                {"timestamp": i, "user": f"user_{i % 2}"}
            )
        
        # Test analytics
        stats = analytics.get_statistics()
        assert stats["total_changes"] == 10
        assert len(stats["unique_states"]) == 3
        assert len(stats["unique_users"]) == 2
        
        # Test pattern detection
        patterns = analytics.detect_patterns()
        assert "frequent_transitions" in patterns
        assert "user_behavior" in patterns

class TestCustomMemorySystems:
    """Test custom memory implementations - THESE WILL FAIL UNTIL YOU IMPLEMENT THEM."""
    
    def test_file_checkpointer(self):
        """
        🧪 Exercise 3.1: Implement file-based checkpointer
        
        You need to create a file checkpointer that:
        1. Saves checkpoints to local files
        2. Implements proper serialization
        3. Handles concurrent access
        4. Provides cleanup mechanisms
        
        📁 Implement in: src/agent/checkpointers.py
        """
        from agent.checkpointers import FileCheckpointer
        
        checkpointer = FileCheckpointer("test_checkpoints")
        
        # Test checkpoint saving
        config = {"thread_id": "test_123"}
        state = {"messages": ["hello", "world"], "counter": 5}
        
        checkpointer.put(config, state, {})
        
        # Test checkpoint loading
        loaded_state = checkpointer.get(config)
        assert loaded_state["messages"] == ["hello", "world"]
        assert loaded_state["counter"] == 5
        
        # Test checkpoint listing
        checkpoints = list(checkpointer.list(config))
        assert len(checkpoints) >= 1
        
        # Cleanup
        checkpointer.cleanup()
    
    def test_redis_checkpointer(self):
        """
        🧪 Exercise 3.2: Implement Redis checkpointer
        
        You need to create a Redis checkpointer that:
        1. Connects to Redis server
        2. Implements efficient serialization
        3. Handles connection failures
        4. Provides TTL support
        
        📁 Implement in: src/agent/checkpointers.py
        Note: This test will be skipped if Redis is not available
        """
        pytest.importorskip("redis", reason="Redis not available")
        
        from agent.checkpointers import RedisCheckpointer
        
        checkpointer = RedisCheckpointer("redis://localhost:6379/0")
        
        # Test connection
        assert checkpointer.is_connected()
        
        # Test checkpoint operations
        config = {"thread_id": "redis_test_123"}
        state = {"messages": ["redis", "test"], "data": {"key": "value"}}
        
        checkpointer.put(config, state, {})
        loaded_state = checkpointer.get(config)
        
        assert loaded_state["messages"] == ["redis", "test"]
        assert loaded_state["data"]["key"] == "value"
        
        # Test TTL
        checkpointer.put(config, state, {}, ttl=1)
        # Note: actual TTL testing would require time.sleep(2)
        
        # Cleanup
        checkpointer.delete(config)
    
    def test_hybrid_memory(self):
        """
        🧪 Exercise 3.3: Create hybrid memory system
        
        You need to create a hybrid memory system that:
        1. Uses multiple storage backends
        2. Implements intelligent routing
        3. Provides fallback mechanisms
        4. Optimizes for different data types
        
        📁 Implement in: src/agent/hybrid_memory.py
        """
        from agent.hybrid_memory import HybridMemorySystem
        
        memory = HybridMemorySystem({
            "fast": "memory",      # In-memory for hot data
            "persistent": "file",  # File storage for cold data
            "distributed": "redis" # Redis for shared data
        })
        
        # Test different data routing
        memory.store("hot_data", {"temp": "value"}, storage_hint="fast")
        memory.store("cold_data", {"archived": "data"}, storage_hint="persistent")
        memory.store("shared_data", {"global": "state"}, storage_hint="distributed")
        
        # Test retrieval
        assert memory.retrieve("hot_data")["temp"] == "value"
        assert memory.retrieve("cold_data")["archived"] == "data"
        
        # Test fallback mechanism
        # Simulate fast storage failure
        memory.disable_storage("fast")
        memory.store("fallback_test", {"data": "fallback"})
        assert memory.retrieve("fallback_test")["data"] == "fallback"
    
    def test_memory_optimization(self):
        """
        🧪 Exercise 3.4: Implement memory optimization
        
        You need to create memory optimizations that:
        1. Implement compression for large states
        2. Use efficient serialization formats
        3. Provide memory usage monitoring
        4. Implement automatic cleanup
        
        📁 Implement in: src/agent/memory_optimizer.py
        """
        from agent.memory_optimizer import MemoryOptimizer
        
        optimizer = MemoryOptimizer()
        
        # Test compression
        large_data = {"messages": ["hello"] * 1000, "data": "x" * 10000}
        compressed = optimizer.compress(large_data)
        
        assert compressed["compressed"] == True
        assert compressed["original_size"] > compressed["compressed_size"]
        
        # Test decompression
        decompressed = optimizer.decompress(compressed)
        assert len(decompressed["messages"]) == 1000
        assert len(decompressed["data"]) == 10000
        
        # Test memory monitoring
        stats = optimizer.get_memory_stats()
        assert "total_memory" in stats
        assert "compression_ratio" in stats

class TestAdvancedToolPatterns:
    """Test advanced tool patterns - THESE WILL FAIL UNTIL YOU IMPLEMENT THEM."""
    
    def test_tool_chains(self):
        """
        🧪 Exercise 4.1: Create tool chains
        
        You need to create a tool chaining system that:
        1. Links tools in sequences
        2. Passes outputs as inputs
        3. Handles chain failures
        4. Provides chain analytics
        
        📁 Implement in: src/agent/tool_chains.py
        """
        from agent.tool_chains import ToolChain
        
        chain = ToolChain([
            {"name": "validate_input", "args": ["data"]},
            {"name": "process_data", "args": ["validated_data"]},
            {"name": "format_output", "args": ["processed_data"]}
        ])
        
        result = chain.execute({"data": {"value": 42}})
        
        assert result["success"] == True
        assert "chain_results" in result
        assert len(result["chain_results"]) == 3
        assert result["final_output"] is not None
    
    def test_tool_caching(self):
        """
        🧪 Exercise 4.2: Implement tool result caching
        
        You need to create a tool caching system that:
        1. Caches tool results intelligently
        2. Implements cache invalidation
        3. Provides cache statistics
        4. Handles cache misses gracefully
        
        📁 Implement in: src/agent/tool_cache.py
        """
        from agent.tool_cache import CachedToolExecutor
        
        executor = CachedToolExecutor(cache_size=100, ttl=300)
        
        # Test cache miss and population
        result1 = executor.execute("expensive_tool", {"param": "value"})
        stats1 = executor.get_cache_stats()
        assert stats1["misses"] == 1
        
        # Test cache hit
        result2 = executor.execute("expensive_tool", {"param": "value"})
        stats2 = executor.get_cache_stats()
        assert stats2["hits"] == 1
        assert result1 == result2
        
        # Test cache invalidation
        executor.invalidate_cache("expensive_tool")
        result3 = executor.execute("expensive_tool", {"param": "value"})
        stats3 = executor.get_cache_stats()
        assert stats3["misses"] == 2
    
    def test_tool_analytics(self):
        """
        🧪 Exercise 4.3: Add tool usage analytics
        
        You need to create tool analytics that:
        1. Tracks tool usage patterns
        2. Measures performance metrics
        3. Identifies optimization opportunities
        4. Provides usage recommendations
        
        📁 Implement in: src/agent/tool_analytics.py
        """
        from agent.tool_analytics import ToolAnalytics
        
        analytics = ToolAnalytics()
        
        # Simulate tool usage
        for i in range(20):
            tool_name = f"tool_{i % 3}"
            duration = 0.1 + (i % 5) * 0.05
            analytics.record_usage(tool_name, duration, success=i % 10 != 0)
        
        # Test analytics
        stats = analytics.get_tool_stats()
        assert len(stats) == 3  # 3 different tools
        
        for tool_stats in stats.values():
            assert "total_calls" in tool_stats
            assert "success_rate" in tool_stats
            assert "avg_duration" in tool_stats
        
        # Test recommendations
        recommendations = analytics.get_recommendations()
        assert "slow_tools" in recommendations
        assert "unreliable_tools" in recommendations
    
    def test_tool_validation(self):
        """
        🧪 Exercise 4.4: Implement tool input/output validation
        
        You need to create tool validation that:
        1. Validates input parameters
        2. Validates output formats
        3. Provides clear error messages
        4. Supports custom validators
        
        📁 Implement in: src/agent/tool_validator.py
        """
        from agent.tool_validator import ValidatedTool
        
        @ValidatedTool(
            input_schema={"type": "object", "properties": {"value": {"type": "number"}}},
            output_schema={"type": "object", "properties": {"result": {"type": "number"}}}
        )
        def math_tool(value: float) -> dict:
            return {"result": value * 2}
        
        # Test valid input/output
        result = math_tool({"value": 5.0})
        assert result["result"] == 10.0
        
        # Test invalid input
        with pytest.raises(ValueError, match="Input validation failed"):
            math_tool({"value": "not_a_number"})
        
        # Test invalid output (simulate)
        with pytest.raises(ValueError, match="Output validation failed"):
            # This would be tested by mocking the function to return invalid output
            pass

class TestErrorHandling:
    """Test error handling patterns - THESE WILL FAIL UNTIL YOU IMPLEMENT THEM."""
    
    def test_retry_logic(self):
        """
        🧪 Exercise 5.1: Implement comprehensive retry logic
        
        You need to create retry mechanisms that:
        1. Handle different error types
        2. Implement multiple retry strategies
        3. Provide retry context
        4. Support custom retry conditions
        
        📁 Implement in: src/agent/retry_handler.py
        """
        from agent.retry_handler import RetryHandler
        
        handler = RetryHandler({
            "max_retries": 3,
            "strategies": ["exponential_backoff", "jitter"],
            "retry_on": ["TimeoutError", "ConnectionError"],
            "base_delay": 0.1
        })
        
        # Test successful retry
        call_count = 0
        def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Temporary failure")
            return "success"
        
        result = handler.retry(flaky_function)
        assert result == "success"
        assert call_count == 3
        
        # Test retry exhaustion
        def always_fails():
            raise TimeoutError("Always fails")
        
        with pytest.raises(TimeoutError):
            handler.retry(always_fails)
    
    def test_circuit_breaker(self):
        """
        🧪 Exercise 5.2: Implement circuit breaker pattern
        
        You need to create a circuit breaker that:
        1. Monitors failure rates
        2. Opens circuit when threshold exceeded
        3. Provides half-open state for testing
        4. Resets automatically on success
        
        📁 Implement in: src/agent/circuit_breaker.py
        """
        from agent.circuit_breaker import CircuitBreaker
        
        breaker = CircuitBreaker(
            failure_threshold=3,
            reset_timeout=1.0,
            success_threshold=2
        )
        
        # Test circuit opening
        for i in range(3):
            with pytest.raises(Exception):
                with breaker:
                    raise Exception(f"Failure {i}")
        
        assert breaker.state == "OPEN"
        
        # Test circuit blocking calls
        with pytest.raises(Exception, match="Circuit breaker is OPEN"):
            with breaker:
                pass
    
    def test_error_recovery(self):
        """
        🧪 Exercise 5.3: Implement error recovery mechanisms
        
        You need to create error recovery that:
        1. Categorizes different error types
        2. Implements recovery strategies
        3. Maintains recovery state
        4. Provides recovery analytics
        
        📁 Implement in: src/agent/error_recovery.py
        """
        from agent.error_recovery import ErrorRecoverySystem
        
        recovery = ErrorRecoverySystem()
        
        # Test error categorization
        error1 = ValueError("Invalid input")
        category1 = recovery.categorize_error(error1)
        assert category1 == "user_error"
        
        error2 = ConnectionError("Network timeout")
        category2 = recovery.categorize_error(error2)
        assert category2 == "network_error"
        
        # Test recovery strategies
        recovery_plan = recovery.get_recovery_plan(error2)
        assert "retry" in recovery_plan["strategies"]
        assert "fallback" in recovery_plan["strategies"]
        
        # Test recovery execution
        result = recovery.execute_recovery(error2, lambda: "recovered")
        assert result == "recovered"
    
    def test_error_monitoring(self):
        """
        🧪 Exercise 5.4: Implement error monitoring and alerting
        
        You need to create error monitoring that:
        1. Tracks error patterns over time
        2. Implements alerting thresholds
        3. Provides error dashboards
        4. Supports custom error handlers
        
        📁 Implement in: src/agent/error_monitor.py
        """
        from agent.error_monitor import ErrorMonitor
        
        monitor = ErrorMonitor()
        
        # Simulate errors
        for i in range(10):
            error = ValueError(f"Error {i}")
            monitor.record_error(error, context={"user": f"user_{i % 3}"})
        
        # Test error statistics
        stats = monitor.get_error_stats()
        assert stats["total_errors"] == 10
        assert len(stats["error_types"]) == 1
        assert len(stats["affected_users"]) == 3
        
        # Test alerting
        alerts = monitor.check_alerts()
        # Depending on thresholds, might have alerts for error rate
        
        # Test error trends
        trends = monitor.get_error_trends(period="1h")
        assert "error_rate" in trends
        assert "trending_errors" in trends


if __name__ == "__main__":
    print()
    print("🚨" * 20)
    print("🚨  LEARNING PLAN 2: TEST-DRIVEN LEARNING  🚨")
    print("🚨" * 20)
    print()
    print("❌ THESE TESTS WILL FAIL - THIS IS EXPECTED!")
    print("✅ Test failures are your learning guide!")
    print()
    print("📋 How to use these tests:")
    print("  1. Run the tests and see them fail")
    print("  2. Read the error message to understand what to implement")
    print("  3. Check the test description for detailed requirements")
    print("  4. Implement the solution in the specified file")
    print("  5. Re-run tests until they pass")
    print("  6. Move to next failing test")
    print()
    print("🛠️  Implementation files to create:")
    print("   • src/agent/custom_nodes.py")
    print("   • src/agent/custom_state.py") 
    print("   • src/agent/state_manager.py")
    print("   • src/agent/checkpointers.py")
    print("   • src/agent/tool_chains.py")
    print("   • And more... (tests will guide you!)")
    print()
    print("🚀 Run with: pytest docs/learning-plans/test_learning_02.py -v")
    print("🚀 Or use: make test-learning PLAN=02")
    print()
    print("🚨" * 20)
