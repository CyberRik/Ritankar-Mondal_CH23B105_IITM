# Multi-Agent System Evaluation Tool

## DS Intern Challenge - 90-Minute Test

This project implements a comprehensive evaluation system for a multi-agent customer service system with the following components:

### Architecture

- **RouterAgent**: Routes customer queries to appropriate sub-agents
- **Sub-Agents**: 
  - SearchAgent: Flight searches, refund status
  - PolicyAgent: Policies, baggage rules, terms
  - ComplaintAgent: Complaints, damage reports
  - BookingAgent: Booking details, confirmations
  - CloserAgent: Conversation termination

### Key Features

- **Conversation Simulation**: Realistic customer query generation
- **Comprehensive Logging**: Detailed tracking of all interactions
- **Metrics Calculation**: Both required and creative metrics
- **Multilingual Support**: English, Spanish, French scenarios
- **V0 vs V1 Analysis**: Comparison of flawed vs improved prompts

### Required Metrics

1. Routing Accuracy
2. Misrouting Count
3. Flow Adherence
4. Tool Call Correctness
5. Router Latency
6. Overall Latency
7. END_CALL Adherence

### Creative Metrics

1. **Agent Overlap Score**: Measures responsibility conflicts
2. **Language Consistency Score**: Tracks language matching
3. **Context Retention Score**: Conversation context maintenance
4. **Tool Efficiency Score**: Optimal tool usage patterns

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run evaluation (single command)
python main.py
```

### Project Structure

```
├── agents/
│   ├── router_agent.py      # RouterAgent implementation
│   ├── sub_agents.py        # All sub-agent implementations
│   └── v1_prompts.py        # Improved v1 prompts
├── simulator/
│   └── customer_simulator.py # Customer query generation
├── evaluation/
│   └── metrics.py           # Metrics calculation
├── main.py                  # Main evaluation system
└── requirements.txt         # Dependencies
```

### V0 Issues Identified

1. **Responsibility Overlaps**: Multiple agents handling same queries
2. **Routing Biases**: Default to SearchAgent when unsure
3. **Language Ignorance**: No language matching
4. **Tool Call Issues**: Multiple calls per turn allowed
5. **END_CALL Misplacement**: Placed at start instead of end

### V1 Improvements

1. **Clear Boundaries**: Each agent has specific responsibilities
2. **Language Matching**: All agents respond in customer's language
3. **Single Agent Rule**: No overlaps or multiple agents per turn
4. **Proper Tool Usage**: One tool call per turn maximum
5. **Correct END_CALL**: Placed at end of CloserAgent response

### Output

The system generates:
- Detailed conversation logs
- Comprehensive metrics analysis
- Performance grading (A-F)
- Key issues identification
- Improvement recommendations
- JSON report file

### Example Usage

```python
from main import MultiAgentEvaluator

evaluator = MultiAgentEvaluator()
report = evaluator.run_evaluation(num_conversations=6)
evaluator.save_report(report)
```

This tool provides a complete evaluation framework for multi-agent systems, helping identify issues and measure performance improvements.
