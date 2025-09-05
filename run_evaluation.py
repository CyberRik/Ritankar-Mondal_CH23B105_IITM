#!/usr/bin/env python3
"""
Quick evaluation runner for the multi-agent system
"""

from main import MultiAgentEvaluator

def run_quick_evaluation():
    """
    Run a quick evaluation with 6 conversations
    """
    print("🚀 Starting Quick Multi-Agent Evaluation")
    print("=" * 50)
    
    # Initialize evaluator
    evaluator = MultiAgentEvaluator()
    
    # Run evaluation
    report = evaluator.run_evaluation(num_conversations=6)
    
    # Save report
    evaluator.save_report(report, "quick_evaluation_report.json")
    
    print(f"\n✅ Quick Evaluation Complete!")
    print(f"📊 Performance Grade: {report['evaluation_summary']['performance_grade']}")
    print(f"📄 Report saved to quick_evaluation_report.json")

if __name__ == "__main__":
    run_quick_evaluation()
