# Integrations — what actually works

Stated plainly, because a repository that overstates its connectors wastes your time.

## What works today

| Integration | Status | Notes |
|---|---|---|
| **Local files** | Working | The agent reads `config/`, `team-data/`, and `skills/`. Zero setup. |
| **Pasting** | Working | Export a report, paste it, ask for the review. The most reliable integration there is. |
| **Local documents** | Working | PDF, DOCX, XLSX, and images in `local_data/`, processed on your machine. |
| **Local AI models** | Working | llama.cpp via a local OpenAI-compatible endpoint. |
| **Cloud AI models** | Working | Whatever you configure in Hermes. |

## What does not exist

| Integration | Status |
|---|---|
| Gmail | **Not implemented** |
| Google Calendar | **Not implemented** |
| Google Drive | **Not implemented** |
| GitHub | **Not implemented** here |
| CRM (any) | **Not implemented** |
| LOS (any) | **Not implemented** |
| Slack | **Not implemented** |

`config/integrations.example.yaml` lists these with `status: placeholder` and
`enabled: false`. They are declared so that a real connector has a standard home when
someone builds one. The Hermes profile ships `mcp_servers: {}` — an empty map, which is
the honest representation of having no connectors.

The agent is instructed to check this file and say "that is not connected" rather than
pretending. If it ever claims otherwise, that is a bug.

## Why pasting is not a cop-out

Every automation in the library is designed around it, and it has real advantages: you
control exactly what the agent sees, there is no OAuth to maintain, no token to leak, and
no vendor API to break. A saved pipeline export takes fifteen minutes to set up once.

## Building a real connector

The supported path is an **MCP server** — Model Context Protocol, the standard Hermes uses
for external tools. Add it under `mcp_servers` in `hermes-home/config.yaml`:

```yaml
mcp_servers:
  my_crm:
    command: "/absolute/path/to/python"
    args: ["-m", "my_crm_mcp.server"]
    tools:
      include: [crm_search, crm_get_pipeline_summary]
```

Guidance if you do:

- **Read-only first.** A connector that can only read cannot corrupt your pipeline.
- **Allow-list the tools.** Use `include`, never expose everything.
- **Keep credentials in `.env`**, never in a tracked file.
- **Treat LOS and CRM data as borrower data.** Read
  [local-ai/privacy-mode.md](local-ai/privacy-mode.md) first.
- **Update `config/integrations.yaml`** to `status: working` so the agent stops disclaiming
  it — and so the documentation stays true.
