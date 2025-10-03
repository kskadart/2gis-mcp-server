# 2GIS Search MCP Server

A simple Model Context Protocol (MCP) server that provides access to the 2GIS Search API. This server allows AI assistants and other MCP clients to search for places, geocode addresses, get location suggestions, and more using the 2GIS mapping service.

## What is This?

This is an MCP server that exposes 2GIS Search API functionality through a standardized protocol. It includes tools for:

- **Places** - Search for places by name and location
- **Geocoder** - Convert addresses to coordinates
- **Suggest** - Get autocomplete suggestions for locations
- **Categories** - Search for business categories
- **Regions** - Find regions by name
- **Markers** - Get map markers for search results

## Prerequisites

- Python 3.13+
- npx (for running MCP Inspector)
- A 2GIS API key

## Getting Your 2GIS API Key

To use this MCP server, you need a 2GIS API key:

1. Visit the [2GIS API Console](https://dev.2gis.com/)
2. Sign up or log in to your account
3. Create a new project
4. Generate an API key for the "Search API"
5. Copy your API key for use in the setup below

**Note:** 2GIS may require you to provide information about your use case and may have geographic or usage restrictions depending on your region.

## Setup

1. **Clone or download this repository**

2. **Create a `.env` file in the project root:**

```bash
DGIS_API_KEY=your_api_key_here
DGIS_SEARCH_API_URL=https://catalog.api.2gis.com
```

Replace `your_api_key_here` with the API key you obtained from 2GIS.

3. **Install dependencies using uv:**

```bash
uv sync
```

## Running the Server

Start the MCP server with:

```bash
python3 -m src.main --transport stdio
```

### Available Options

- `--transport`: Choose transport protocol (`stdio`, `sse`, or `streamable-http`). Default: `stdio`
- `--host`: Host to bind the server to. Default: `0.0.0.0`
- `--port`: Port to bind the server to. Default: `8101`
- `--debug`: Enable debug mode for verbose logging

Example with custom port and debug mode:
```bash
uv run src/main.py --transport streamable-http --host 0.0.0.0 --port 8101 --debug
```

### Running with Docker

The easiest way to run the server is using Docker Compose with streamable-http transport:

```bash
# Start the server
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop the server
docker-compose down
```

The Docker container runs with streamable-http transport on port 8101, making it accessible at `http://localhost:8101`.

### Testing with MCP Inspector

#### Testing stdio transport (local development):

```bash
npx @modelcontextprotocol/inspector uv run src/main.py --transport stdio
```

#### Testing streamable-http transport (Docker):

1. **Start the MCP Inspector:**
   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. **Open your browser** and navigate to `http://localhost:6274`

3. **Connect to your server:**
   - Transport type: Select **"SSE"** or **"HTTP"**
   - URL: Enter `http://localhost:8101/mcp` (for SSE) or `http://localhost:8101` (for HTTP)
   - Click **"Connect"**

4. **Test your tools** - You should now see all 6 available tools and can test them interactively!

## Available Tools

Once running, the MCP server exposes the following tools:

- `place_tool(query, location, point, radius)` - Search for places
- `geocoder_tool(query, location)` - Geocode addresses
- `suggest_tool(query, location)` - Get location suggestions
- `categories_tool(query, region_id)` - Search categories
- `regions_tool(query)` - Search regions
- `markers_tool(query, location)` - Get map markers

## Testing 2GIS API Directly

The `https/` directory contains `.http` files for testing the 2GIS API endpoints directly. These files can be used with REST client extensions (like REST Client for VS Code or IntelliJ HTTP Client) to explore and verify the API responses:

- `geocode.http` - Test geocoding endpoints
- `suggest.http` - Test autocomplete suggestions
- `place.http` - Test place search
- `categories.http` - Test category search
- `regions.http` - Test region search
- `markers.http` - Test marker endpoints

**To use these files:**
1. Configure your API key in `.vscode/settings.json` (see `.vscode/settings.json.example` for reference)
2. Open any `.http` file in your IDE
3. Click "Send Request" (or equivalent in your IDE)
4. View the API response directly

These are useful for understanding the raw 2GIS API responses before testing through the MCP server.

## Documentation

For detailed 2GIS API documentation, see the [official 2GIS Search API documentation](https://docs.2gis.com/en/api/search/overview).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
