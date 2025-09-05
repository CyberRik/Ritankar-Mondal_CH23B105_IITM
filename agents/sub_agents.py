import json
import time
import random
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod

class BaseSubAgent(ABC):
    """Base class for all sub-agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.response_history = []
        self.tool_calls = []
    
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
        message_lower = message.lower()
        tool_calls = []
        response = ""
        
        # Handle refund status queries
        if "refund status" in message_lower or "booking id" in message_lower:
            # Extract booking ID (simplified)
            booking_id = self._extract_booking_id(message)
            tool_calls.append({
                "action": "refund_status",
                "params": {"booking_id": booking_id}
            })
            response = f"I'll check the refund status for booking ID {booking_id}."
        
        # Handle flight search
        elif any(word in message_lower for word in ["search", "find", "flight"]):
            # Assume defaults (flawed behavior)
            tool_calls.append({
                "action": "search_flights",
                "params": {
                    "origin": "BLR",
                    "destination": "DEL", 
                    "date": "today",
                    "class": "economy"
                }
            })
            response = "I'll search for flights with the default parameters."
        
        # Handle refund policies (overlap with PolicyAgent)
        elif "refund policy" in message_lower:
            response = "Refunds are processed within 5-7 business days. (SearchAgent handling policy query)"
        
        else:
            response = "I can help you with flight searches and refund status. What would you like to know?"
        
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
        message_lower = message.lower()
        tool_calls = []
        response = ""
        
        # Handle baggage policy
        if "baggage" in message_lower or "allowance" in message_lower:
            response = "Domestic flights allow 15kg check-in and 7kg cabin baggage. International flights allow 23kg check-in and 7kg cabin baggage."
        
        # Handle refund policy
        elif "refund policy" in message_lower:
            response = "Refunds are processed within 5-7 business days. Processing fees may apply."
        
        # Handle refund status (overlap with SearchAgent)
        elif "refund status" in message_lower:
            booking_id = self._extract_booking_id(message)
            tool_calls.append({
                "action": "refund_status",
                "params": {"booking_id": booking_id}
            })
            response = f"I'll check the refund status for booking ID {booking_id}. (PolicyAgent also handling this)"
        
        # Check bookings directly (flawed behavior)
        elif "booking" in message_lower:
            tool_calls.append({
                "action": "check_booking",
                "params": {"booking_id": 12345}
            })
            response = "I'll check your booking details directly."
        
        else:
            response = "I can help you with policies and refund information. What would you like to know?"
        
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
        message_lower = message.lower()
        tool_calls = []
        response = ""
        
        # Handle luggage damage
        if "damage" in message_lower or "luggage" in message_lower:
            tool_calls.append({
                "action": "file_complaint",
                "params": {
                    "type": "luggage_damage",
                    "description": message
                }
            })
            response = "I'm sorry to hear about the luggage damage. I'll file a complaint for you."
        
        # Handle general complaints
        elif any(word in message_lower for word in ["complaint", "problem", "issue", "bad"]):
            tool_calls.append({
                "action": "file_complaint",
                "params": {
                    "type": "general",
                    "description": message
                }
            })
            response = "I understand your concern. I'll file a complaint and have someone follow up with you."
        
        # Handle refund status (overlap with other agents)
        elif "refund" in message_lower:
            response = "I can help you with refund status. Let me check that for you. (ComplaintAgent handling refund)"
        
        else:
            response = "I'm here to help with complaints and issues. Please tell me what happened."
        
        self.log_response(message, response, tool_calls)
        return response, tool_calls

class BookingAgent(BaseSubAgent):
    """BookingAgent v0 - Handles passenger details and confirmations"""
    
    def __init__(self):
        super().__init__("BookingAgent")
    
    def respond(self, message: str, context: List[Dict] = None) -> Tuple[str, List[Dict]]:
        message_lower = message.lower()
        tool_calls = []
        response = ""
        
        # Handle passenger details
        if any(word in message_lower for word in ["passenger", "details", "name", "contact"]):
            tool_calls.append({
                "action": "get_passenger_details",
                "params": {"booking_id": 12345}
            })
            response = "I'll retrieve the passenger details for your booking."
        
        # Handle booking confirmation
        elif "confirm" in message_lower or "confirmation" in message_lower:
            tool_calls.append({
                "action": "confirm_booking",
                "params": {"booking_id": 12345}
            })
            response = "I'll confirm your booking details."
        
        # Handle availability (flawed behavior - should be SearchAgent)
        elif "available" in message_lower or "availability" in message_lower:
            tool_calls.append({
                "action": "check_availability",
                "params": {"route": "BLR-DEL", "date": "today"}
            })
            response = "I'll check flight availability for you. (BookingAgent handling availability)"
        
        else:
            response = "I can help you with booking details and confirmations. What do you need?"
        
        self.log_response(message, response, tool_calls)
        return response, tool_calls

class CloserAgent(BaseSubAgent):
    """CloserAgent v0 - Closes conversations"""
    
    def __init__(self):
        super().__init__("CloserAgent")
    
    def respond(self, message: str, context: List[Dict] = None) -> Tuple[str, List[Dict]]:
        tool_calls = []
        
        # v0 flawed behavior - places END_CALL at start
        response = "<END_CALL> Thank you for contacting us. Have a great day!"
        
        self.log_response(message, response, tool_calls)
        return response, tool_calls
