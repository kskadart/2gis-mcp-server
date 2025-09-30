"""
2GIS Search MCP Server

This server provides a Machine Control Protocol (MCP) interface for interacting with the 2GIS Search APIs.
The Server includes next APIs: 
- Places
- Geocoder
- Suggest
- Categories
- Regions
- Markers

Original API doc: https://docs.2gis.com/en/api/search/overview
"""

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from src.settings import dgis_api_settings
from src.logger import logger


mcp = FastMCP("2gis-search-mcp", host="0.0.0.0", port=8000)


class DGisSearchAPI:
    """2GIS API client class"""
    
    def __init__(self, api_key: str, url: str):
        """
        Initialize 2GIS API client
        
        Args:
            api_key: API key for 2GIS API
            url: Base URL for 2GIS API
        """
        self.api_key = api_key
        self.url = url

    def place_api(self, query: str, location: str, point: str, radius: int = 1000) -> dict[str, Any]:
        """
        Place API

        Args:
            query: str - place 
            location: str - location in format "latitude,longitude"
            point: str - point in format "latitude,longitude"
            radius: int - radius in meters (default: 1000)

        Returns:
            dict - response from 2GIS Place API
        """
        logger.info(f"Place API request: query='{query}', location='{location}', point='{point}', radius={radius}")
        
        try:
            response: httpx.Response = httpx.get(
                f"{self.url}/3.0/items",
                params={
                    "q": query,
                    "point": point,
                    "location": location,
                    "radius": radius,
                    "sort": "distance",
                    "key": self.api_key,
                },
            )
            response.raise_for_status()
            logger.debug(f"Place API response status: {response.status_code}")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Place API error: {str(e)}")
            raise
            
    def geocoder_api(self, query: str, location: str | None = None) -> dict[str, Any]:
        """
        Geocoder API

        Args:
            query: str - query
            location: str - location in format "latitude,longitude" (optional)
        Returns:
            dict - response from 2GIS Geocoder API
        """
        logger.info(f"Geocoder API request: query='{query}', location='{location}'")
        
        try:
            response: httpx.Response = httpx.get(
                f"{self.url}/3.0/items/geocode",
                params={
                    "q": query,
                    "location": location,
                    "key": self.api_key,
                },
            )
            response.raise_for_status()
            logger.debug(f"Geocoder API response status: {response.status_code}")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Geocoder API error: {str(e)}")
            raise
        
    def suggest_api(self, query: str, location: str | None = None) -> dict[str, Any]:
        """
        Suggest API

        Args:
            query: str - query
            location: str - location in format "latitude,longitude" (optional)
        Returns:
            dict - response from 2GIS Suggest API
        """
        logger.info(f"Suggest API request: query='{query}', location='{location}'")
        
        try:
            response: httpx.Response = httpx.get(
                f"{self.url}/3.0/items/suggests",
                params={
                    "q": query,
                    "location": location,
                    "key": self.api_key,
                },
            )
            response.raise_for_status()
            logger.debug(f"Suggest API response status: {response.status_code}")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Suggest API error: {str(e)}")
            raise
        
    def categories_api(self, query: str, region_id: int = 1) -> dict[str, Any]:
        """
        Categories API

        Args:
            query: str - query
            region_id: int - region ID
        Returns:
            dict - response from 2GIS Categories API
        """
        logger.info(f"Categories API request: query='{query}', region_id={region_id}")
        
        try:
            response: httpx.Response = httpx.get(
                f"{self.url}/2.0/catalog/rubric/search",
                params={
                    "q": query,
                    "region_id": region_id,
                    "key": self.api_key,
                },
            )
            response.raise_for_status()
            logger.debug(f"Categories API response status: {response.status_code}")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Categories API error: {str(e)}")
            raise
        
    def regions_api(self, query: str) -> dict[str, Any]:
        """
        Regions API

        Args:
            query: str - search by a region name
        Returns:
            dict - response from 2GIS Regions API
        """
        logger.info(f"Regions API request: query='{query}'")
        
        try:
            response: httpx.Response = httpx.get(
                f"{self.url}/2.0/region/search",
                params={
                    "q": query,
                    "key": self.api_key,
                },
            )
            response.raise_for_status()
            logger.debug(f"Regions API response status: {response.status_code}")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Regions API error: {str(e)}")
            raise
        
    def markers_api(self, query: str, location: str | None = None) -> dict[str, Any]:
        """
        Markers API

        Args:
            query: str - query
            location: str - location in format "latitude,longitude"
        Returns:
            dict - response from 2GIS Markers API
        """
        logger.info(f"Markers API request: query='{query}', location='{location}'")
        
        try:
            response: httpx.Response = httpx.get(
                f"{self.url}/3.0/markers",
                params={
                    "q": query,
                    "location": location,
                    "key": self.api_key,
                },
            )
            response.raise_for_status()
            logger.debug(f"Markers API response status: {response.status_code}")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Markers API error: {str(e)}")
            raise


dgis_search_api = DGisSearchAPI(
    api_key=dgis_api_settings.api_key,
    url=dgis_api_settings.search_api_url
)


@mcp.tool()
def categories_api(query: str, region_id: int = 1) -> dict[str, Any]:
    """
    Categories API

    Args:
        query: str - query
        region_id: int - region ID
    Returns:
        dict - response from 2GIS Categories API
    """
    logger.info(f"MCP Categories API request: query='{query}', region_id={region_id}")
    
    try:
        result = dgis_search_api.categories_api(query, region_id)
        logger.debug("MCP Categories API response received successfully")
        return result
    except Exception as e:
        logger.error(f"MCP Categories API error: {str(e)}")
        raise


@mcp.tool()
def geocoder_api(query: str, location: str | None = None) -> dict[str, Any]:
    """
    Geocoder API

    Args:
        query: str - query
        location: str - location in format "latitude,longitude" (optional)
    Returns:
        dict - response from 2GIS Geocoder API
    """
    logger.info(f"MCP Geocoder API request: query='{query}', location='{location}'")
    
    try:
        result = dgis_search_api.geocoder_api(query, location)
        logger.debug("MCP Geocoder API response received successfully")
        return result
    except Exception as e:
        logger.error(f"MCP Geocoder API error: {str(e)}")
        raise


@mcp.tool()
def markers_api(query: str, location: str | None = None) -> dict[str, Any]:
    """
    Markers API

    Args:
        query: str - query
        location: str - location in format "latitude,longitude"
    Returns:
        dict - response from 2GIS Markers API
    """
    logger.info(f"MCP Markers API request: query='{query}', location='{location}'")
    
    try:
        result = dgis_search_api.markers_api(query, location)
        logger.debug("MCP Markers API response received successfully")
        return result
    except Exception as e:
        logger.error(f"MCP Markers API error: {str(e)}")
        raise


@mcp.tool()
def place_api(query: str, location: str, point: str, radius: int = 1000) -> dict[str, Any]:
    """
    Place API

    Args:
        query: str - place 
        location: str - location in format "latitude,longitude"
        point: str - point in format "latitude,longitude"
        radius: int - radius in meters

    Returns:
        dict - response from 2GIS Place API
    """
    logger.info(f"MCP Place API request: query='{query}', location='{location}', point='{point}', radius={radius}")
    
    try:
        result = dgis_search_api.place_api(query, location, point, radius)
        logger.debug("MCP Place API response received successfully")
        return result
    except Exception as e:
        logger.error(f"MCP Place API error: {str(e)}")
        raise


@mcp.tool()
def regions_api(query: str) -> dict[str, Any]:
    """
    Regions API

    Args:
        query: str - search by a region name
    Returns:
        dict - response from 2GIS Regions API
    """
    logger.info(f"MCP Regions API request: query='{query}'")
    
    try:
        result = dgis_search_api.regions_api(query)
        logger.debug("MCP Regions API response received successfully")
        return result
    except Exception as e:
        logger.error(f"MCP Regions API error: {str(e)}")
        raise


@mcp.tool()
def suggest_api(query: str, location: str | None = None) -> dict[str, Any]:
    """
    Suggest API

    Args:
        query: str - query
        location: str - location in format "latitude,longitude" (optional)
    Returns:
        dict - response from 2GIS Suggest API
    """
    logger.info(f"MCP Suggest API request: query='{query}', location='{location}'")
    
    try:
        result = dgis_search_api.suggest_api(query, location)
        logger.debug("MCP Suggest API response received successfully")
        return result
    except Exception as e:
        logger.error(f"MCP Suggest API error: {str(e)}")
        raise
