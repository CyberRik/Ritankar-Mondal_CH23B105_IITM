#!/usr/bin/env python3
"""
Multi-Agent System Evaluation Tool
DS Intern Challenge - 90-Minute Test
"""

import json
import time
import random
from typing import List, Dict
from datetime import datetime

from agents.router_agent import RouterAgent
from agents.sub_agents import SearchAgent, PolicyAgent, ComplaintAgent, BookingAgent, CloserAgent
from simulator.customer_simulator import CustomerSimulator
from evaluation.metrics import MetricsCalculator

class MultiAgentEvaluator:
    """
    Main evaluation system for multi-agent customer service
    """
    
    def __init__(self):
        self.router = RouterAgent()
        self.agents = {
            "SearchAgent": SearchAgent(),
            "PolicyAgent": PolicyAgent(),
            "ComplaintAgent": ComplaintAgent(),
            "BookingAgent": BookingAgent(),
            "CloserAgent": CloserAgent()
        }
        self.customer_simulator = CustomerSimulator()
        self.metrics_calculator = MetricsCalculator()
        self.conversation_logs = []
    
    def run_evaluation(self, num_conversations: int = 6) -> Dict:
        """
        Run complete evaluation with specified number of conversations
        """
        print(f"🚀 Starting Multi-Agent System Evaluation")
        print(f"📊 Running {num_conversations} conversations...")
        print("=" * 60)
        
        # Generate and run conversations
        for i in range(num_conversations):
            print(f"\n🔄 Running Conversation {i+1}/{num_conversations}")
            conversation_log = self._run_single_conversation(i+1)
            self.conversation_logs.append(conversation_log)
            self.metrics_calculator.add_conversation_log(conversation_log)
        
        # Calculate metrics
        print(f"\n📈 Calculating Metrics...")
        metrics = self.metrics_calculator.calculate_all_metrics()
        
        # Generate report
        report = self._generate_evaluation_report(metrics)
        
        return report
    
    def _run_single_conversation(self, conv_id: int) -> Dict:
        """
        Run a single conversation and return detailed log
        """
        # Generate conversation scenario
        scenario_types = ["refund_status", "flight_search", "baggage_policy", "complaint", "booking_details", "mixed"]
        scenario_type = random.choice(scenario_types)
        
        # Add multilingual test
        if conv_id == 6:
            conversation = self.customer_simulator.generate_multilingual_conversation()
        else:
            conversation = self.customer_simulator.generate_conversation(scenario_type)
        
        print(f"   📝 Scenario: {scenario_type}")
        print(f"   💬 Messages: {len(conversation)} turns")
        
        # Run conversation
        turns = []
        for turn_data in conversation:
            turn_log = self._process_turn(conv_id, turn_data)
            turns.append(turn_log)
            
            # Print turn summary
            print(f"      Turn {turn_data['turn_id']}: {turn_data['message'][:50]}...")
            print(f"         → Routed to: {turn_log['routed_agent']}")
            if turn_log['tool_calls']:
                print(f"         → Tool calls: {len(turn_log['tool_calls'])}")
        
        return {
            "conversation_id": conv_id,
            "scenario_type": scenario_type,
            "language": conversation[0]["language"] if conversation else "english",
            "turns": turns,
            "timestamp": datetime.now().isoformat()
        }
    
    def _process_turn(self, conv_id: int, turn_data: Dict) -> Dict:
        """
        Process a single turn in the conversation
        """
        start_time = time.time()
        
        # Router decides which agent to use
        routed_agent, router_latency = self.router.route(turn_data["message"])
        
        # Get response from selected agent
        agent = self.agents[routed_agent]
        response, tool_calls = agent.respond(turn_data["message"])
        
        overall_latency = time.time() - start_time
        
        return {
            "conversation_id": conv_id,
            "turn_id": turn_data["turn_id"],
            "customer_message": turn_data["message"],
            "category": turn_data["category"],
            "routed_agent": routed_agent,
            "agent_response": response,
            "tool_calls": tool_calls,
            "router_latency": router_latency,
            "overall_latency": overall_latency,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_evaluation_report(self, metrics: Dict) -> Dict:
        """
        Generate comprehensive evaluation report
        """
        print(f"\n📋 Generating Evaluation Report...")
        
        report = {
            "evaluation_summary": {
                "total_conversations": len(self.conversation_logs),
                "total_turns": sum(len(conv["turns"]) for conv in self.conversation_logs),
                "evaluation_timestamp": datetime.now().isoformat(),
                "performance_grade": metrics["summary"]["performance_grade"]
            },
            "required_metrics": metrics["required_metrics"],
            "creative_metrics": metrics["creative_metrics"],
            "conversation_logs": self.conversation_logs,
            "analysis": {
                "key_issues": metrics["summary"]["key_issues"],
                "recommendations": self._generate_recommendations(metrics)
            }
        }
        
        # Print summary
        self._print_metrics_summary(metrics)
        
        return report
    
    def _print_metrics_summary(self, metrics: Dict):
        """
        Print metrics summary to console
        """
        print("\n" + "=" * 60)
        print("📊 EVALUATION RESULTS SUMMARY")
        print("=" * 60)
        
        print(f"\n🎯 Required Metrics:")
        req_metrics = metrics["required_metrics"]
        print(f"   • Routing Accuracy: {req_metrics['routing_accuracy']:.1f}%")
        print(f"   • Misrouting Count: {req_metrics['misrouting_count']}")
        print(f"   • Flow Adherence: {req_metrics['flow_adherence']:.1f}%")
        print(f"   • Tool Call Correctness: {req_metrics['tool_call_correctness']:.1f}%")
        print(f"   • Router Latency: {req_metrics['router_latency_avg']:.3f}s")
        print(f"   • Overall Latency: {req_metrics['overall_latency_avg']:.3f}s")
        print(f"   • END_CALL Adherence: {req_metrics['end_call_adherence']:.1f}%")
        
        print(f"\n🎨 Creative Metrics:")
        creative_metrics = metrics["creative_metrics"]
        print(f"   • Agent Overlap Score: {creative_metrics['agent_overlap_score']:.2f}")
        print(f"   • Language Consistency: {creative_metrics['language_consistency_score']:.1f}%")
        print(f"   • Context Retention: {creative_metrics['context_retention_score']:.2f}")
        print(f"   • Tool Efficiency: {creative_metrics['tool_efficiency_score']:.2f}")
        
        print(f"\n🏆 Overall Performance Grade: {metrics['summary']['performance_grade']}")
        
        if metrics["summary"]["key_issues"]:
            print(f"\n⚠️  Key Issues Identified:")
            for issue in metrics["summary"]["key_issues"]:
                print(f"   • {issue}")
    
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """
        Generate recommendations based on metrics analysis
        """
        recommendations = []
        
        if metrics["required_metrics"]["routing_accuracy"] < 80:
            recommendations.append("Improve router logic to reduce misrouting")
        
        if metrics["creative_metrics"]["agent_overlap_score"] > 0.3:
            recommendations.append("Clarify agent responsibilities to reduce overlaps")
        
        if metrics["required_metrics"]["tool_call_correctness"] < 90:
            recommendations.append("Fix tool call format and validation")
        
        if metrics["required_metrics"]["end_call_adherence"] < 100:
            recommendations.append("Ensure CloserAgent places END_CALL at end of response")
        
        return recommendations
    
    def save_report(self, report: Dict, filename: str = "evaluation_report.json"):
        """
        Save evaluation report to file
        """
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 Report saved to {filename}")

def main():
    """
    Main execution function
    """
    print("🤖 Multi-Agent System Evaluation Tool")
    print("DS Intern Challenge - 90-Minute Test")
    print("=" * 60)
    
    # Initialize evaluator
    evaluator = MultiAgentEvaluator()
    
    # Run evaluation
    report = evaluator.run_evaluation(num_conversations=6)
    
    # Save report
    evaluator.save_report(report)
    
    # Print detailed summary
    print(f"\n📊 FINAL RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total Conversations: {report['evaluation_summary']['total_conversations']}")
    print(f"Total Turns: {report['evaluation_summary']['total_turns']}")
    print(f"Performance Grade: {report['evaluation_summary']['performance_grade']}")
    
    print(f"\n🎯 Required Metrics:")
    for metric, value in report['required_metrics'].items():
        print(f"  • {metric}: {value}")
    
    print(f"\n🎨 Creative Metrics:")
    for metric, value in report['creative_metrics'].items():
        print(f"  • {metric}: {value}")
    
    print(f"\n⚠️ Key Issues:")
    for issue in report['analysis']['key_issues']:
        print(f"  • {issue}")
    
    print(f"\n💡 Recommendations:")
    for rec in report['analysis']['recommendations']:
        print(f"  • {rec}")
    
    print(f"\n✅ Evaluation Complete!")
    print(f"📄 Detailed report saved to evaluation_report.json")
    print(f"📄 Analysis report saved to analysis_report.md")
    print(f"📄 V0 failure analysis saved to V0_FAILURE_ANALYSIS.md")

if __name__ == "__main__":
    main()
