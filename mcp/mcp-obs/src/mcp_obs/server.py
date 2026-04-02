#!/usr/bin/env python3
"""MCP server for observability tools (VictoriaLogs and VictoriaTraces)."""
import asyncio
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-obs")

VICTORIALOGS_URL = "http://localhost:42010"
VICTORIATRACES_URL = "http://localhost:42011"

@mcp.tool()
async def logs_search(query: str = "_time:1h", limit: int = 100) -> str:
    """Search VictoriaLogs by LogsQL query.
    
    Args:
        query: LogsQL query (e.g., '_time:1h severity:ERROR service.name:backend')
        limit: Maximum number of log entries to return
    
    Returns:
        JSON response with log entries
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{VICTORIALOGS_URL}/select/logsql/query",
            params={"query": query, "limit": limit},
            timeout=30
        )
        return resp.text

@mcp.tool()
async def logs_error_count(hours: int = 1) -> str:
    """Count errors per service over a time window.
    
    Args:
        hours: Time window in hours (default: 1)
    
    Returns:
        Count of errors grouped by service
    """
    query = f"_time:{hours}h severity:ERROR | stats count() by service.name"
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{VICTORIALOGS_URL}/select/logsql/query",
            params={"query": query},
            timeout=30
        )
        return resp.text

@mcp.tool()
async def traces_search(service: str = "Learning Management Service", limit: int = 10) -> str:
    """Search traces by service name.
    
    Args:
        service: Service name to filter traces
        limit: Maximum number of traces to return
    
    Returns:
        JSON response with trace information
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{VICTORIATRACES_URL}/select/jaeger/api/traces",
            params={"service": service, "limit": limit},
            timeout=30
        )
        return resp.text

@mcp.tool()
async def trace_details(trace_id: str) -> str:
    """Get detailed span hierarchy for a specific trace.
    
    Args:
        trace_id: The trace ID to look up
    
    Returns:
        JSON response with full trace span hierarchy
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{VICTORIATRACES_URL}/select/jaeger/api/traces/{trace_id}",
            timeout=30
        )
        return resp.text

def main():
    """Run the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()
