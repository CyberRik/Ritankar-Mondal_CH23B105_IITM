import time
from typing import List, Dict, Any
from collections import defaultdict

class MetricsCalculator:
    """
    Calculate evaluation metrics for multi-agent system
    """
    
    def __init__(self):
        self.conversation_logs = []
        self.required_metrics = {}
        self.creative_metrics = {}
    
    def add_conversation_log(self, conversation_log: Dict):
        """Add conversation log for analysis"""
        self.conversation_logs.append(conversation_log)
    
    def calculate_all_metrics(self) -> Dict[str, Any]:
        """Calculate all required and creative metrics"""
        self._calculate_required_metrics()
        self._calculate_creative_metrics()
        
        return {
            "required_metrics": self.required_metrics,
            "creative_metrics": self.creative_metrics,
            "summary": self._generate_summary()
        }
    
    def _calculate_required_metrics(self):
        """Calculate all required metrics"""
        total_turns = 0
        correct_routings = 0
        misroutings = 0
        tool_calls_correct = 0
        tool_calls_total = 0
        end_call_correct = 0
        end_call_total = 0
        router_latencies = []
        overall_latencies = []
        flow_violations = 0
        
        for conv in self.conversation_logs:
            for turn in conv["turns"]:
                total_turns += 1
                
                # Routing accuracy
                expected_agent = self._get_expected_agent(turn["customer_message"], turn["category"])
                if turn["routed_agent"] == expected_agent:
                    correct_routings += 1
                else:
                    misroutings += 1
                
                # Tool call correctness
                for tool_call in turn.get("tool_calls", []):
                    tool_calls_total += 1
                    if self._is_valid_tool_call(tool_call):
                        tool_calls_correct += 1
                
                # END_CALL adherence
                if turn["routed_agent"] == "CloserAgent":
                    end_call_total += 1
                    if "<END_CALL>" in turn.get("agent_response", ""):
                        end_call_correct += 1
                
                # Latency metrics
                router_latencies.append(turn.get("router_latency", 0))
                overall_latencies.append(turn.get("overall_latency", 0))
                
                # Flow adherence
                if not self._check_flow_adherence(turn, conv["turns"]):
                    flow_violations += 1
        
        # Calculate metrics
        self.required_metrics = {
            "routing_accuracy": (correct_routings / total_turns * 100) if total_turns > 0 else 0,
            "misrouting_count": misroutings,
            "flow_adherence": ((total_turns - flow_violations) / total_turns * 100) if total_turns > 0 else 0,
            "tool_call_correctness": (tool_calls_correct / tool_calls_total * 100) if tool_calls_total > 0 else 0,
            "router_latency_avg": sum(router_latencies) / len(router_latencies) if router_latencies else 0,
            "overall_latency_avg": sum(overall_latencies) / len(overall_latencies) if overall_latencies else 0,
            "end_call_adherence": (end_call_correct / end_call_total * 100) if end_call_total > 0 else 0
        }
    
    def _calculate_creative_metrics(self):
        """Calculate creative metrics"""
        agent_overlaps = 0
        language_mismatches = 0
        context_retention_score = 0
        tool_efficiency_score = 0
        
        for conv in self.conversation_logs:
            # Agent Overlap Score
            agent_overlaps += self._count_agent_overlaps(conv)
            
            # Language Consistency Score
            language_mismatches += self._count_language_mismatches(conv)
            
            # Context Retention Score
            context_retention_score += self._calculate_context_retention(conv)
            
            # Tool Efficiency Score
            tool_efficiency_score += self._calculate_tool_efficiency(conv)
        
        total_conversations = len(self.conversation_logs)
        
        self.creative_metrics = {
            "agent_overlap_score": agent_overlaps / total_conversations if total_conversations > 0 else 0,
            "language_consistency_score": (1 - language_mismatches / total_conversations) * 100 if total_conversations > 0 else 0,
            "context_retention_score": context_retention_score / total_conversations if total_conversations > 0 else 0,
            "tool_efficiency_score": tool_efficiency_score / total_conversations if total_conversations > 0 else 0
        }
    
    def _get_expected_agent(self, message: str, category: str) -> str:
        """Determine expected agent based on message content and category"""
        message_lower = message.lower()
        
        if category == "refund_status":
            return "SearchAgent"
        elif category == "refund_policy":
            return "PolicyAgent"
        elif category == "flight_search":
            return "SearchAgent"
        elif category == "baggage_policy":
            return "PolicyAgent"
        elif category == "complaint":
            return "ComplaintAgent"
        elif category == "booking_details":
            return "BookingAgent"
        else:
            return "SearchAgent"  # Default
    
    def _is_valid_tool_call(self, tool_call: Dict) -> bool:
        """Check if tool call is valid"""
        required_fields = ["action", "params"]
        return all(field in tool_call for field in required_fields)
    
    def _check_flow_adherence(self, turn: Dict, all_turns: List[Dict]) -> bool:
        """Check if conversation flow is proper"""
        # Basic flow check - CloserAgent should only appear at the end
        if turn["routed_agent"] == "CloserAgent":
            turn_index = all_turns.index(turn)
            return turn_index == len(all_turns) - 1
        return True
    
    def _count_agent_overlaps(self, conv: Dict) -> int:
        """Count overlapping responsibilities in conversation"""
        overlaps = 0
        agent_responsibilities = defaultdict(list)
        
        for turn in conv["turns"]:
            agent = turn["routed_agent"]
            category = turn.get("category", "unknown")
            agent_responsibilities[agent].append(category)
        
        # Check for overlaps
        for agent, responsibilities in agent_responsibilities.items():
            if len(set(responsibilities)) > 1:
                overlaps += 1
        
        return overlaps
    
    def _count_language_mismatches(self, conv: Dict) -> int:
        """Count language mismatches between customer and agent"""
        mismatches = 0
        expected_language = conv.get("language", "english")
        
        for turn in conv["turns"]:
            # Simple language detection (in real implementation, use proper NLP)
            if expected_language != "english" and not any(word in turn.get("agent_response", "").lower() for word in ["hola", "gracias", "bonjour", "merci"]):
                mismatches += 1
        
        return mismatches
    
    def _calculate_context_retention(self, conv: Dict) -> float:
        """Calculate how well agents maintain conversation context"""
        context_score = 0
        total_turns = len(conv["turns"])
        
        for i, turn in enumerate(conv["turns"]):
            if i > 0:
                # Check if current response references previous context
                prev_turn = conv["turns"][i-1]
                if any(word in turn.get("agent_response", "").lower() for word in prev_turn.get("customer_message", "").lower().split()[:3]):
                    context_score += 1
        
        return context_score / max(total_turns - 1, 1)
    
    def _calculate_tool_efficiency(self, conv: Dict) -> float:
        """Calculate tool usage efficiency"""
        total_tool_calls = sum(len(turn["tool_calls"]) for turn in conv["turns"])
        total_turns = len(conv["turns"])
        
        # Optimal tool usage: 1 tool call per turn when needed
        optimal_calls = total_turns * 0.5  # Assume 50% of turns need tools
        efficiency = 1 - abs(total_tool_calls - optimal_calls) / max(optimal_calls, 1)
        
        return max(0, efficiency)
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary of all metrics"""
        return {
            "total_conversations": len(self.conversation_logs),
            "total_turns": sum(len(conv["turns"]) for conv in self.conversation_logs),
            "performance_grade": self._calculate_performance_grade(),
            "key_issues": self._identify_key_issues()
        }
    
    def _calculate_performance_grade(self) -> str:
        """Calculate overall performance grade"""
        avg_accuracy = self.required_metrics.get("routing_accuracy", 0)
        
        if avg_accuracy >= 90:
            return "A"
        elif avg_accuracy >= 80:
            return "B"
        elif avg_accuracy >= 70:
            return "C"
        elif avg_accuracy >= 60:
            return "D"
        else:
            return "F"
    
    def _identify_key_issues(self) -> List[str]:
        """Identify key issues from metrics"""
        issues = []
        
        if self.required_metrics.get("routing_accuracy", 0) < 80:
            issues.append("Low routing accuracy")
        
        if self.required_metrics.get("tool_call_correctness", 0) < 90:
            issues.append("Tool call issues")
        
        if self.required_metrics.get("end_call_adherence", 0) < 100:
            issues.append("END_CALL placement issues")
        
        if self.creative_metrics.get("agent_overlap_score", 0) > 0.5:
            issues.append("Agent responsibility overlaps")
        
        return issues
