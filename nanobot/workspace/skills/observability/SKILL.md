---
name: observability
description: Use observability tools to investigate errors and diagnose failures
always: true
---

# Observability Skill

## When user asks "What went wrong?" or "Check system health":

1. **Call logs_error_count** for the last hour to see if there are errors
2. **Call logs_search** with query "_time:1h severity:ERROR" to get error details
3. **Extract trace_id** from the error logs
4. **Call traces_get** with the trace_id to see the full failure trace
5. **Summarize findings**: mention the service, the error, and the trace evidence

## When user asks about specific errors:

- Use logs_search with the specific query
- Extract trace_id if available
- Call traces_get for full context
- Summarize concisely

## Response format:

- Start with the conclusion (what failed)
- Cite log evidence (error message, timestamp)
- Cite trace evidence (trace_id, failing span)
- Name the affected service and operation
