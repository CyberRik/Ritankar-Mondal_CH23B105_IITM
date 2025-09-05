import json
import time
import random
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod
from .llm_client import LLMClient

class BaseSubAgent(ABC):
    """Base class for all sub-agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.response_history = []
        self.tool_calls = []
        self.llm_client = LLMClient()
    
    @abstractmethod
    def respond(self, message: str, context: List[Dict] = None) -> Tuple[str, List[Dict]]:
        """
        Generate response to customer message
        Returns: (response_text, tool_calls)
        """
        pass
    
    def log_response(self, message: str, response: str, tool_calls: List[Dict]):
        """Log agent response"""
        self.response_history.append({
            "input_message": message,
            "response": response,
            "tool_calls": tool_calls,
            "timestamp": time.time()
        })

class SearchAgent(BaseSubAgent):
    """SearchAgent v0 - Handles flight searches, refund status, and sometimes refund policies"""
    
    def __init__(self):
        super().__init__("SearchAgent")
    
    def respond(self, message: str, context: List[Dict] = None) -> Tuple[str, List[Dict]]:
        response, tool_calls = self.llm_client.search_agent_response(message, context)
        self.log_response(message, response, tool_calls)
        return response, tool_calls
    
    def _extract_booking_id(self, message: str) -> int:
        """Extract booking ID from message (simplified)"""
        import re
        numbers = re.findall(r'\d+', message)
        return int(numbers[0]) if numbers else 12345

class PolicyAgent(BaseSubAgent):
    """PolicyAgent v0 - Handles refund policies, baggage allowances, and refund status"""
    
    def __init__(self):
        super().__init__("PolicyAgent")
    
    def respond(self, message: str, context: List[Dict] = None) -> Tuple[str, List[Dict]]:
        response, tool_calls = self.llm_client.policy_agent_response(message, context)
        self.log_response(message, response, tool_calls)
        return response, tool_calls
    
    def _extract_booking_id(self, message: str) -> int:
        """Extract booking ID from message (simplified)"""
        import re
        numbers = re.findall(r'\d+', message)
        return int(numbers[0]) if numbers else 12345

class ComplaintAgent(BaseSubAgent):
    """ComplaintAgent v0 - Handles damaged luggage or complaints"""
    
    def __init__(self):
        super().__init__("ComplaintAgent")
    
    def respond(self, message: str, context: List[Dict] = None) -> Tuple[str, List[Dict]]:
        response, tool_calls = self.llm_client.complaint_agent_response(message, context)
        self.log_response(message, response, tool_calls)
        return response, tool_calls

class BookingAgent(BaseSubAgent):
    """BookingAgent v0 - Handles passenger details and confirmations"""
    
    def __init__(self):
        super().__init__("BookingAgent")
    
    def respond(self, message: str, context: List[Dict] = None) -> Tuple[str, List[Dict]]:
        response, tool_calls = self.llm_client.booking_agent_response(message, context)
        self.log_response(message, response, tool_calls)
        return response, tool_calls

class CloserAgent(BaseSubAgent):
    """CloserAgent v0 - Closes conversations"""
    
    def __init__(self):
        super().__init__("CloserAgent")
    
    def respond(self, message: str, context: List[Dict] = None) -> Tuple[str, List[Dict]]:
        response, tool_calls = self.llm_client.closer_agent_response(message, context)
        self.log_response(message, response, tool_calls)
        return response, tool_calls
