# mcp-kayak

`mcp-kayak` is a prototype server implementing the **Model Context Protocol** (MCP). It is designed for use by agent frameworks such as Claude to query flight information. The server currently consumes the **Travelpayouts API** to return flight options including price, duration and transfers for a given origin, destination, date and travel class. Over time it will expand to aggregate results from multiple providers.

This project is inspired by [clickhouse-mcp](https://github.com/izaitsevfb/clickhouse-mcp) and will evolve to support multiple providers and parallel queries.

## Usage

### Installation

0. Create a virtual environment (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

1. Install this package with pip. You can either install directly from GitHub
   or from a local clone:

   ```bash
   pip install "mcp-kayak@git+https://github.com/wdvr/mcp-kayak.git"
   ```

   Or if you have cloned the repository:

   ```bash
   pip install -e .
   ```

2. Copy `.env.template` to `.env` and fill in the required variables.

3. Add this MCP server to Claude:

   ```bash
   claude mcp add-json kayak '{ "type": "stdio", "command": "python", "args": [ "-m", "mcp_kayak" ], "env": {} }'
   ```

4. Run Claude as usual:

   ```bash
   claude
   ```

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
   curl -X POST https://api.travelpayouts.com/v1/flight_search \
     -H 'Content-Type: application/json' \
     -d '{"signature":"'$TRAVELPAYOUTS_APIKEY'","segments":[{"origin":"NYC","destination":"LAX","date":"2025-01-01"}]}'
   ```
   A valid key will return JSON instead of an `Unauthorized` message.
   Optionally set `TRAVELPAYOUTS_CURRENCY` to control the currency used for
   flight prices (defaults to `USD`).

3. Start the server using the MCP CLI with the Inspector:

```bash
mcp dev mcp_kayak.server:server
```

The MCP Inspector will open in your browser and connect to the running server.

### Frontend

This repository also ships a simple Next.js UI under `frontend` that lets you
query flights through a local `claude` installation.

```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:3000> to use the interface. Queries are executed locally
with `claude -p` through the API route `/api/query`.

### Endpoints

- `GET /ping` – health check.
- `GET /airports?location=<city>` – return the closest airport codes for a city or country name.
- `GET /flights?origin=<code>&destination=<code>&date=YYYY-MM-DD&cabin=<class>&return_date=YYYY-MM-DD&include_return=<bool>` – search for flight options. When `include_return` is true (the default), return flights are also shown. The `return_date` parameter can specify a different date for the return leg.

## Testing and CI

Run the linters and tests locally with:

```bash
pip install -r requirements.txt
pre-commit install
pre-commit run --all-files
pytest -q
```

All pull requests are checked by the CI workflows, which run `ruff` and
`pytest`. Mark the workflows as required in the repository settings to block
merges when they fail.
