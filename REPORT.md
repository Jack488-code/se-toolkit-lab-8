# Lab 8 — Report

## Task 1A — Bare agent

**Question: "What is the agentic loop?"**

The agentic loop is the fundamental cycle that an AI agent follows to accomplish tasks autonomously. It typically consists of these core stages:

1. **Perceive** — Gather information about the current state (user input, environment, tool outputs, memory)
2. **Reason/Plan** — Analyze the situation, determine goals, and decide on next actions
3. **Act** — Execute actions using available tools (file operations, API calls, shell commands, etc.)
4. **Observe** — Receive feedback from the actions taken (success, failure, output data)
5. **Iterate** — Repeat the loop until the goal is achieved or a stopping condition is met

This loop enables agents to break complex tasks into steps, adapt based on feedback, use tools dynamically, handle errors and retry, and maintain context across iterations.

**Question: "What labs are available in our LMS?"** (bare agent without MCP)

The bare agent has no access to the LMS backend. It explored local files instead:

> Based on my exploration of the workspace, here's what I found about the available labs in your LMS:
>
> **Lab 8 (current workspace): se-toolkit-lab-8**
>
> - This is the main lab you're working on in this repository (se-toolkit-lab-8)
> - Focus: Building an AI agent (nanobot) as a natural-language interface to the LMS
>
> **Lab 1**
>
> - Located at /root/se-toolkit-lab-8/wiki/lab-1/
> - Contains documentation and diagrams

The agent inspected local files but could not query the live LMS backend.

---

## Task 1B — Agent with LMS tools

**Question: "What labs are available in our LMS?"** (with MCP tools)

After adding MCP LMS tools, the agent returns real data from the backend:

> Here are the available labs in the LMS:
>
> 1. Lab 01 – Products, Architecture & Roles
> 2. Lab 02 — Run, Fix, and Deploy a Backend Service
> 3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
> 4. Lab 04 — Testing, Front-end, and AI Agents
> 5. Lab 05 — Data Pipeline and Analytics Dashboard
> 6. Lab 06 — Build Your Own Agent
> 7. Lab 07 — Build a Client with an AI Coding Agent
> 8. lab-08

The agent successfully called `mcp_lms_lms_labs({})` and returned real lab names from the LMS backend.

---

## Task 1C — Skill prompt

**Question: "Show me the scores"** (without specifying a lab)

After adding the LMS skill prompt, the agent asks for clarification instead of guessing:

> There are 8 labs available. Which lab would you like to see the scores for? Here are the options:
>
> 1. Lab 01 – Products, Architecture & Roles
> 2. Lab 02 — Run, Fix, and Deploy a Backend Service
> 3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
> 4. Lab 04 — Testing, Front-end, and AI Agents
> 5. Lab 05 — Data Pipeline and Analytics Dashboard
> 6. Lab 06 — Build Your Own Agent
> 7. Lab 07 — Build a Client with an AI Coding Agent
> 8. lab-08
>
> Or would you like to see scores for all labs?

The skill prompt teaches the agent to call `lms_labs` first when a lab parameter is missing, then ask the user to choose.

## Task 2A — Deployed agent

**Nanobot gateway startup log excerpt:**

```
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | 2026-04-01 00:20:56.339 | INFO     | nanobot.channels.manager:_init_channels:58 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | 2026-04-01 00:20:56.795 | INFO     | nanobot.channels.manager:start_all:91 - Starting webchat channel...
nanobot-1  | 2026-04-01 00:20:58.279 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_health' from server 'lms'
nanobot-1  | 2026-04-01 00:20:58.280 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
```

**Files modified:**

- `nanobot/Dockerfile` — Multi-stage build with nanobot-ai installed
- `nanobot/entrypoint.py` — Resolves environment variables into config at runtime
- `docker-compose.yml` — Added nanobot service with volumes for mcp and nanobot-websocket-channel
- `caddy/Caddyfile` — Added `handle /ws/chat` route proxying to nanobot

---

## Task 2B — Web client

**WebSocket endpoint:** `http://localhost:42002/ws/chat?access_key=YOUR_NANOBOT_ACCESS_KEY`

**Flutter UI:** `http://localhost:42002/flutter/`

**Setup steps:**

1. Cloned `nanobot-websocket-channel` submodule
2. Installed `nanobot-webchat` and `mcp-webchat` packages
3. Enabled webchat channel in `nanobot/config.json`
4. Uncommented `client-web-flutter` service in `docker-compose.yml`
5. Uncommented `/flutter*` route in `caddy/Caddyfile`

**Conversation excerpt:**

```
User: Hello! What can you do?
Agent: I'm nanobot, your personal AI assistant. I can help you with:
- File & Directory Operations
- Web Access
- Command Execution
- Subagents
- LMS queries (labs, pass rates, learners, etc.)
```

*[Screenshot of Flutter chat UI would be added here]*

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
