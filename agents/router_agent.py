import json
import time
from typing import Dict, List, Optional, Tuple

class RouterAgent:
    """
    Router Agent v0 - Decides which sub-agent should respond
    """
    
    def __init__(self):
        self.available_agents = [
            "SearchAgent", "PolicyAgent", "ComplaintAgent", 
            "BookingAgent", "CloserAgent"
        ]
        self.routing_history = []
        
    def route(self, customer_message: str, conversation_context: List[Dict] = None) -> Tuple[str, float]:
        """
        Route customer message to appropriate sub-agent
        Returns: (selected_agent, routing_time)
        """
        start_time = time.time()
        
        # v0 flawed routing logic
        selected_agent = self._route_v0(customer_message, conversation_context)
        
        routing_time = time.time() - start_time
        
        # Log routing decision
        self.routing_history.append({
            "message": customer_message,
            "selected_agent": selected_agent,
            "routing_time": routing_time,
            "timestamp": time.time()
        })
        
        return selected_agent, routing_time
    
    def _route_v0(self, message: str, context: List[Dict] = None) -> str:
        """
        v0 Flawed routing logic with known issues:
        - Defaults to SearchAgent when unsure
        - Allows multiple agents for same turn
        - Ignores language requirements
        - Keyword-based only
        """
        message_lower = message.lower()
        
        # Check for end conversation signals
        if any(word in message_lower for word in ["bye", "goodbye", "end", "close", "finish"]):
            return "CloserAgent"
        
        # Keyword-based routing (flawed approach)
        if any(word in message_lower for word in ["search", "find", "flight", "refund status", "booking id"]):
            return "SearchAgent"
        
        if any(word in message_lower for word in ["policy", "baggage", "allowance", "refund policy"]):
            return "PolicyAgent"
        
        if any(word in message_lower for word in ["complaint", "damage", "problem", "issue"]):
            return "ComplaintAgent"
        
        if any(word in message_lower for word in ["booking", "passenger", "details", "confirm"]):
            return "BookingAgent"
        
        # Default to SearchAgent (flawed rule)
        return "SearchAgent"
    
    def get_routing_history(self) -> List[Dict]:
        """Get complete routing history"""
        return self.routing_history
