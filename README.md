# mcp-kayak

`mcp-kayak` is a prototype server implementing the **Model Context Protocol** (MCP). It is designed for use by agent frameworks such as Claude to query flight information. The server currently consumes the **Travelpayouts API** to return flight options including price, duration and transfers for a given origin, destination, date and travel class. Over time it will expand to aggregate results from multiple providers.

This project is inspired by [clickhouse-mcp](https://github.com/izaitsevfb/clickhouse-mcp) and will evolve to support multiple providers and parallel queries.

## Development

See `AGENTS.md` for contribution guidelines. Planned tasks are listed in `PLAN.txt` and linked to [GitHub issues](https://github.com/wdvr/mcp-kayak/issues).

## Running locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Adjust configuration by editing `.env` if needed. The file is loaded automatically via `python-dotenv`.
   Sign up on [Travelpayouts](https://www.travelpayouts.com/) and obtain an API token.
   Set the token as `TRAVELPAYOUTS_APIKEY` in your environment. You can verify
   the token works with a quick `curl` call:

   ```bash
   curl -G https://api.travelpayouts.com/aviasales/v3/prices_for_dates \
     --data-urlencode origin=NYC \
     --data-urlencode destination=LAX \
     --data-urlencode depart_date=2025-01-01 \
     --data-urlencode token=$TRAVELPAYOUTS_APIKEY
   ```
   A valid key will return JSON instead of an `Unauthorized` message.

3. Start the server using the MCP CLI with the Inspector:

```bash
mcp dev mcp_kayak.server:server
```

The MCP Inspector will open in your browser and connect to the running server.

## Testing and CI

Run the linters and tests locally with:

```bash
pip install -r requirements.txt
pip install flake8
flake8
pytest -q
```

All pull requests are checked by the `CI` workflow, which runs `flake8` and
`pytest`. Mark the workflow as required in the repository settings to block
merges when it fails.
