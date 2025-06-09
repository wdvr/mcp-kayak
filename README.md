# mcp-kayak

`mcp-kayak` is a prototype server implementing the **Model Context Protocol** (MCP). It is designed for use by agent frameworks such as Claude to query flight information. The server consumes the Kayak API (it does not implement it) to return flight options including price, duration and transfers for a given origin, destination, date and travel class. Over time it will expand to aggregate results from multiple providers.

This project is inspired by [clickhouse-mcp](https://github.com/izaitsevfb/clickhouse-mcp) and will evolve to support multiple providers and parallel queries.

## Development

See `AGENTS.md` for contribution guidelines. Planned tasks are listed in `PLAN.txt` and linked to [GitHub issues](https://github.com/wdvr/mcp-kayak/issues).
To create GitHub issues programmatically, set the `GITHUB_TOKEN` (or `GH_TOKEN`) environment variable with a token that has access to the repository. If the token is missing, CLI commands such as `gh issue create` will prompt for login and fail in non-interactive environments.
Example `curl` command to create an issue:

```bash
curl -X POST https://api.github.com/repos/OWNER/REPO/issues \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{"title": "Issue title", "body": "Issue body"}'
```
