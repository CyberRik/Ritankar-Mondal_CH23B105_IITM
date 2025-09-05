import requests
import json
from typing import Dict, List

class LLMClient:
    """
    Client for calling GPT-4o-Mini API
    """
    
    def __init__(self):
        self.url = "https://reasearch-interns.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
        self.headers = {
            "Content-Type": "application/json",
            "api-key": "cc3b2035419042a381b6d95df5585085"
        }
    
    def call_llm(self, messages: List[Dict], max_tokens: int = 20) -> str:
        """
        Call GPT-4o-Mini API with given messages
        """
        data = {
            "messages": messages,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return "I'm sorry, I'm having trouble processing your request right now."
    
    def route_message(self, message: str, context: List[Dict] = None) -> str:
        """
        Use RouterAgent v0 prompt to route message
        """
        router_prompt = """You are the Router Agent. Decide which sub-agent should respond. Available: SearchAgent, PolicyAgent, ComplaintAgent, BookingAgent, CloserAgent. Rules: 1) Always output one sub-agent, but if unsure, pick SearchAgent by default. 2) You may let two agents handle the same turn if both are relevant. 3) If the user ends, you can either pick CloserAgent or just end the chat directly. 4) Language doesn't matter — pick based on keywords only.

Customer message: {message}

Respond with just the agent name:"""
        
        messages = [
            {"role": "system", "content": router_prompt.format(message=message)},
            {"role": "user", "content": message}
        ]
        
        response = self.call_llm(messages, max_tokens=20)
        
        # Clean up response to get agent name
        for agent in ["SearchAgent", "PolicyAgent", "ComplaintAgent", "BookingAgent", "CloserAgent"]:
            if agent in response:
                return agent
        
        return "SearchAgent"  # Default fallback
    
    def search_agent_response(self, message: str, context: List[Dict] = None) -> tuple:
        """
        Use SearchAgent v0 prompt to respond
        """
        search_prompt = """You are SearchAgent. You handle flight searches, refund status, and sometimes refund policies. If missing details, assume defaults (economy, today's date). Multiple tool calls per turn are okay.

Customer message: {message}

Respond naturally and use <CALL_TOOL=action>{{"param":"value"}} format for tool calls if needed."""
        
        messages = [
            {"role": "system", "content": search_prompt.format(message=message)},
            {"role": "user", "content": message}
        ]
        
        response = self.call_llm(messages, max_tokens=150)
        
        # Extract tool calls from response
        tool_calls = []
        if "<CALL_TOOL=" in response:
            # Simple tool call extraction (in real implementation, use proper parsing)
            if "refund_status" in response:
                tool_calls.append({"action": "refund_status", "params": {"booking_id": 12345}})
            elif "search_flights" in response:
                tool_calls.append({"action": "search_flights", "params": {"origin": "BLR", "destination": "DEL", "date": "today", "class": "economy"}})
        
        return response, tool_calls
    
    def policy_agent_response(self, message: str, context: List[Dict] = None) -> tuple:
        """
        Use PolicyAgent v0 prompt to respond
        """
        policy_prompt = """You are PolicyAgent. You handle refund policies, baggage allowances, and refund status. If unsure, may also check bookings directly.

Customer message: {message}

Respond naturally and use <CALL_TOOL=action>{{"param":"value"}} format for tool calls if needed."""
        
        messages = [
            {"role": "system", "content": policy_prompt.format(message=message)},
            {"role": "user", "content": message}
        ]
        
        response = self.call_llm(messages, max_tokens=150)
        
        # Extract tool calls from response
        tool_calls = []
        if "<CALL_TOOL=" in response:
            if "refund_status" in response:
                tool_calls.append({"action": "refund_status", "params": {"booking_id": 12345}})
            elif "check_booking" in response:
                tool_calls.append({"action": "check_booking", "params": {"booking_id": 12345}})
        
        return response, tool_calls
    
    def complaint_agent_response(self, message: str, context: List[Dict] = None) -> tuple:
        """
        Use ComplaintAgent v0 prompt to respond
        """
        complaint_prompt = """You are ComplaintAgent. You handle damaged luggage or complaints. If refund comes up, may also answer refund status.

Customer message: {message}

Respond naturally and use <CALL_TOOL=action>{{"param":"value"}} format for tool calls if needed."""
        
        messages = [
            {"role": "system", "content": complaint_prompt.format(message=message)},
            {"role": "user", "content": message}
        ]
        
        response = self.call_llm(messages, max_tokens=150)
        
        # Extract tool calls from response
        tool_calls = []
        if "<CALL_TOOL=" in response:
            if "file_complaint" in response:
                tool_calls.append({"action": "file_complaint", "params": {"type": "general", "description": message}})
        
        return response, tool_calls
    
    def booking_agent_response(self, message: str, context: List[Dict] = None) -> tuple:
        """
        Use BookingAgent v0 prompt to respond
        """
        booking_prompt = """You are BookingAgent. You handle passenger details and confirmations. If user asks availability, you may also handle it.

Customer message: {message}

Respond naturally and use <CALL_TOOL=action>{{"param":"value"}} format for tool calls if needed."""
        
        messages = [
            {"role": "system", "content": booking_prompt.format(message=message)},
            {"role": "user", "content": message}
        ]
        
        response = self.call_llm(messages, max_tokens=150)
        
        # Extract tool calls from response
        tool_calls = []
        if "<CALL_TOOL=" in response:
            if "get_booking_details" in response:
                tool_calls.append({"action": "get_booking_details", "params": {"booking_id": 12345}})
            elif "check_availability" in response:
                tool_calls.append({"action": "check_availability", "params": {"route": "BLR-DEL", "date": "today"}})
        
        return response, tool_calls
    
    def closer_agent_response(self, message: str, context: List[Dict] = None) -> tuple:
        """
        Use CloserAgent v0 prompt to respond
        """
        closer_prompt = """You are CloserAgent. You close conversations. Place <END_CALL> at start of final message. You may close early if you think it's done.

Customer message: {message}

Respond naturally with <END_CALL> at the start."""
        
        messages = [
            {"role": "system", "content": closer_prompt.format(message=message)},
            {"role": "user", "content": message}
        ]
        
        response = self.call_llm(messages, max_tokens=100)
        
        return response, []
