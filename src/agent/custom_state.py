"""
Custom State Management for Learning Plan 2

🎯 This file contains STUB implementations for advanced state management.
You need to complete these implementations to make the tests pass.
"""

from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import MessagesState


class ValidatedState(MessagesState):
    """
    🧪 Exercise 2.1: State class with validation
    
    TODO: Implement a state class that validates its fields.
    
    Required fields:
    - messages: List (inherited from MessagesState)
    - user_id: str (required, non-empty)
    - session_data: dict (optional, must be dict if provided)
    - metadata: dict (optional)
    
    Required methods:
    - is_valid() -> bool
    - validate_field(field_name: str, value: Any) -> bool
    """
    
    user_id: str
    session_data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __init__(self, **kwargs):
        # TODO: Implement validation logic in constructor
        # Validate user_id is not empty
        # Validate session_data is dict if provided
        # Call parent constructor
        
        # This is a placeholder that will make tests fail
        raise NotImplementedError("You need to implement ValidatedState.__init__")
    
    def is_valid(self) -> bool:
        """Check if current state is valid."""
        # TODO: Implement comprehensive validation
        raise NotImplementedError("You need to implement is_valid method")
    
    def validate_field(self, field_name: str, value: Any) -> bool:
        """Validate a specific field value."""
        # TODO: Implement field-specific validation
        raise NotImplementedError("You need to implement validate_field method")
