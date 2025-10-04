import argparse
import logging
import signal
import os

from mcp.server.fastmcp import FastMCP
from src.dgis_search_mcp import (
    categories_tool,
    regions_tool,
    suggest_tool,
    place_tool,
    markers_tool,
    geocoder_tool,
)
from src.logger import logger


parser = argparse.ArgumentParser(description="2Gis MCP Server")
parser.add_argument(
    "--transport",
    choices=["stdio", "sse", "streamable-http"],
    default="stdio",
    help="Transport protocol to use",
)
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to (default: 0.0.0.0)")
parser.add_argument("--port", type=int, default=8101, help="Port to bind the server to (default: 8101)")


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    os._exit(0)


def main():
    args = parser.parse_args()

    # Configure logger based on debug mode
    log_level = logging.DEBUG if args.debug else logging.INFO
    logger.setLevel(log_level)

    # Initialize MCP with parsed host and port
    mcp = FastMCP("2gis-search-mcp", host=args.host, port=args.port)
    mcp.add_tool(categories_tool)
    mcp.add_tool(geocoder_tool)
    mcp.add_tool(markers_tool)
    mcp.add_tool(place_tool)
    mcp.add_tool(regions_tool)
    mcp.add_tool(suggest_tool)

    if args.debug:
        logger.debug("Debug mode enabled")
        mcp.debug = True

    logger.info("Start 2GIS MCP Server")
    logger.info(f"Args: transport: {args.transport}, host: {args.host}, port: {args.port}, debug: {args.debug}")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        mcp.run(transport=args.transport)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
    except Exception as e:
        logger.error(f"Error starting MCP server: {str(e)}")
        os._exit(1)


if __name__ == "__main__":
    main()
