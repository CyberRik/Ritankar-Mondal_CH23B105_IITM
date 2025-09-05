import random
from typing import List, Dict

class CustomerSimulator:
    """
    Agent J - Simulates customer interactions
    Generates realistic customer queries in multiple languages
    """
    
    def __init__(self):
        self.conversation_scenarios = [
            # Refund scenarios
            {
                "category": "refund_status",
                "messages": [
                    "Check my refund status for booking ID 456",
                    "When will I get my refund?",
                    "I need to know about my refund for booking 789"
                ]
            },
            {
                "category": "refund_policy", 
                "messages": [
                    "What is your refund policy?",
                    "Can I get a refund for my flight?",
                    "What are the refund terms and conditions?"
                ]
            },
            # Flight search scenarios
            {
                "category": "flight_search",
                "messages": [
                    "Find me a flight from BLR to DEL on September 15",
                    "I need flights from Mumbai to Bangalore tomorrow",
                    "Search for flights to New York next week"
                ]
            },
            # Baggage policy scenarios
            {
                "category": "baggage_policy",
                "messages": [
                    "What is the baggage allowance for domestic flights?",
                    "How much luggage can I carry?",
                    "What are the baggage rules for international flights?"
                ]
            },
            # Complaint scenarios
            {
                "category": "complaint",
                "messages": [
                    "My luggage was damaged during the flight",
                    "I have a complaint about the service",
                    "The staff was very rude to me"
                ]
            },
            # Booking scenarios
            {
                "category": "booking_details",
                "messages": [
                    "Can you confirm my booking details?",
                    "I need to update my passenger information",
                    "What are the details for booking 12345?"
                ]
            },
            # Mixed scenarios (to test routing)
            {
                "category": "mixed",
                "messages": [
                    "I want to book a flight and also check my refund status",
                    "What's the baggage policy and can I get a refund?",
                    "I have a complaint and need to search for flights"
                ]
            }
        ]
        
        # Multilingual scenarios
        self.multilingual_scenarios = [
            {
                "language": "spanish",
                "messages": [
                    "Necesito verificar el estado de mi reembolso",
                    "¿Cuál es la política de equipaje?",
                    "Quiero buscar un vuelo de Madrid a Barcelona"
                ]
            },
            {
                "language": "french", 
                "messages": [
                    "Je voudrais vérifier le statut de mon remboursement",
                    "Quelle est la politique de bagages?",
                    "Je cherche un vol de Paris à Lyon"
                ]
            }
        ]
    
    def generate_conversation(self, scenario_type: str = "random", language: str = "english") -> List[Dict]:
        """
        Generate a conversation with 4-6 turns
        """
        if scenario_type == "random":
            scenario = random.choice(self.conversation_scenarios)
        else:
            scenario = next((s for s in self.conversation_scenarios if s["category"] == scenario_type), 
                          self.conversation_scenarios[0])
        
        # Select 4-6 messages randomly
        num_turns = random.randint(4, 6)
        selected_messages = random.sample(scenario["messages"], min(num_turns, len(scenario["messages"])))
        
        # Add follow-up messages to make it more realistic
        conversation = []
        for i, message in enumerate(selected_messages):
            conversation.append({
                "turn_id": i + 1,
                "message": message,
                "category": scenario["category"],
                "language": language
            })
        
        return conversation
    
    def generate_multilingual_conversation(self) -> List[Dict]:
        """Generate conversation in non-English language"""
        scenario = random.choice(self.multilingual_scenarios)
        return self.generate_conversation(scenario_type="refund_status", language=scenario["language"])
    
    def get_all_scenarios(self) -> List[str]:
        """Get list of all available scenario categories"""
        return [scenario["category"] for scenario in self.conversation_scenarios]
