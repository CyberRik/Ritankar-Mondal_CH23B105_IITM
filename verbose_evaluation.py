#!/usr/bin/env python3
"""
Verbose evaluation runner with detailed output
"""

from main import MultiAgentEvaluator
import json

def run_verbose_evaluation():
    print('🚀 Starting Verbose Multi-Agent Evaluation')
    print('=' * 60)
    
    evaluator = MultiAgentEvaluator()
    report = evaluator.run_evaluation(num_conversations=6)
    
    print('\n📊 FINAL RESULTS SUMMARY')
    print('=' * 60)
    print(f'Total Conversations: {report["evaluation_summary"]["total_conversations"]}')
    print(f'Total Turns: {report["evaluation_summary"]["total_turns"]}')
    print(f'Performance Grade: {report["evaluation_summary"]["performance_grade"]}')
    
    print('\n🎯 Required Metrics:')
    for metric, value in report['required_metrics'].items():
        print(f'  • {metric}: {value}')
    
    print('\n🎨 Creative Metrics:')
    for metric, value in report['creative_metrics'].items():
        print(f'  • {metric}: {value}')
    
    print('\n⚠️ Key Issues:')
    for issue in report['analysis']['key_issues']:
        print(f'  • {issue}')
    
    print('\n💡 Recommendations:')
    for rec in report['analysis']['recommendations']:
        print(f'  • {rec}')
    
    print('\n✅ Evaluation Complete!')
    print('📄 Detailed report saved to evaluation_report.json')
    print('📄 Analysis report saved to analysis_report.md')

if __name__ == "__main__":
    run_verbose_evaluation()
