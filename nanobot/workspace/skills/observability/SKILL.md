---
name: obs
description: Use observability MCP tools for logs and traces
always: true
---

# Observability Skill

You have access to VictoriaLogs and VictoriaTraces via MCP tools. Use them to investigate system health and failures.

## Available Tools

- `mcp_obs_logs_search` — Search logs by LogsQL query
- `mcp_obs_logs_error_count` — Count errors per service over a time window
- `mcp_obs_traces_search` — Search traces by service name
- `mcp_obs_trace_details` — Get full span hierarchy for a trace

## Strategy Rules

### When user asks about errors or failures:
1. First call `mcp_obs_logs_error_count(hours=1)` to see if there are errors
2. If errors exist, call `mcp_obs_logs_search(query="_time:1h severity:ERROR", limit=10)` to get details
3. If the user asks "what went wrong?" or "diagnose the failure":
   - Search logs for ERROR entries
   - Extract the `trace_id` from error logs
   - Call `mcp_obs_trace_details(trace_id=<id>)` to see the full span hierarchy
   - Identify which service/span caused the failure
   - Report the root cause clearly

### When user asks about system health:
1. Call `mcp_obs_logs_error_count(hours=1)` to check for recent errors
2. Call `mcp_obs_traces_search(service="Learning Management Service", limit=5)` to see recent traces
3. Report: "System is healthy" or "Found X errors in the last hour: [details]"

### Query examples:
- `_time:1h severity:ERROR` — errors in the last hour
- `_time:1h service.name:backend` — backend logs in the last hour
- `_time:10m severity:ERROR db_query` — database errors in the last 10 minutes

### Formatting:
- Keep responses concise
- Include timestamps and trace IDs when relevant
- Explain what each tool found before moving to the next
