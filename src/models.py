from pydantic import BaseModel, model_validator, computed_field


class GeocoderParams(BaseModel):
    """Geocoder API parameters with validation"""
    
    class Config:
        extra = "forbid"
    
    query: str = ""
    lat: float | None = None
    lon: float | None = None
    fields: str = "items.point"
    
    @computed_field
    @property
    def location(self) -> str | None:
        """Construct location string from lat/lon if both are provided"""
        if self.lat is not None and self.lon is not None:
            return f"{self.lat},{self.lon}"
        return None
    
    @model_validator(mode='after')
    def validate_at_least_one_param(self) -> 'GeocoderParams':
        """Validate that at least one of query or (lat and lon) is provided"""
        # If only one of lat/lon is provided, that's an error (check this first)
        if (self.lat is None) != (self.lon is None):
            raise ValueError("Both 'lat' and 'lon' must be provided together")
        
        # Check if we have a valid query
        has_query = bool(self.query)
        
        # Check if we have both lat and lon
        has_location = self.lat is not None and self.lon is not None
        
        # Need at least one
        if not has_query and not has_location:
            raise ValueError("At least one of 'query' or both 'lat' and 'lon' must be provided")
        
        return self
