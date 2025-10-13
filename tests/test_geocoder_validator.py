"""Tests for Geocoder Pydantic validator"""

import pytest
from pydantic import ValidationError

from src.models import GeocoderParams


def test_geocoder_params_with_query_only():
    """Test that GeocoderParams accepts query without location"""
    params = GeocoderParams(query="Moscow")
    assert params.query == "Moscow"
    assert params.lat is None
    assert params.lon is None
    assert params.fields == "items.point"


def test_geocoder_params_with_location_only():
    """Test that GeocoderParams accepts lat/lon without query"""
    params = GeocoderParams(lat=55.751244, lon=37.618423)
    assert not params.query  # Query should be None or empty
    assert params.lat == 55.751244
    assert params.lon == 37.618423
    assert params.fields == "items.point"


def test_geocoder_params_with_both():
    """Test that GeocoderParams accepts both query and lat/lon"""
    params = GeocoderParams(query="Red Square", lat=55.751244, lon=37.618423)
    assert params.query == "Red Square"
    assert params.lat == 55.751244
    assert params.lon == 37.618423
    assert params.fields == "items.point"


def test_geocoder_params_with_custom_fields():
    """Test that GeocoderParams accepts custom fields parameter"""
    params = GeocoderParams(query="Moscow", fields="items.point,items.address")
    assert params.query == "Moscow"
    assert params.fields == "items.point,items.address"


def test_geocoder_params_fails_without_any_params():
    """Test that GeocoderParams raises ValueError when no parameters are provided"""
    with pytest.raises(ValidationError) as exc_info:
        GeocoderParams()
    
    # Check that the error message contains our custom validation message
    assert "At least one of 'query' or both 'lat' and 'lon' must be provided" in str(exc_info.value)


def test_geocoder_params_fails_with_empty_query_only():
    """Test that GeocoderParams raises ValueError when only empty query is provided"""
    with pytest.raises(ValidationError) as exc_info:
        GeocoderParams(query="")
    
    # Check that the error message contains our custom validation message
    assert "At least one of 'query' or both 'lat' and 'lon' must be provided" in str(exc_info.value)


def test_geocoder_params_fails_with_only_lat():
    """Test that GeocoderParams raises ValueError when only lat is provided"""
    with pytest.raises(ValidationError) as exc_info:
        GeocoderParams(lat=55.751244)
    
    # Check that the error message contains our custom validation message
    assert "Both 'lat' and 'lon' must be provided together" in str(exc_info.value)


def test_geocoder_params_fails_with_only_lon():
    """Test that GeocoderParams raises ValueError when only lon is provided"""
    with pytest.raises(ValidationError) as exc_info:
        GeocoderParams(lon=37.618423)
    
    # Check that the error message contains our custom validation message
    assert "Both 'lat' and 'lon' must be provided together" in str(exc_info.value)


def test_geocoder_params_fails_with_empty_query_and_only_lat():
    """Test that GeocoderParams raises ValueError when empty query and only lat is provided"""
    with pytest.raises(ValidationError) as exc_info:
        GeocoderParams(query="", lat=55.751244)
    
    # Check that the error message contains our custom validation message
    assert "Both 'lat' and 'lon' must be provided together" in str(exc_info.value)

