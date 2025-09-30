from pydantic import Field
from pydantic_settings import BaseSettings


class DGISAPISettings(BaseSettings):
    api_key: str = Field(..., description="API key for 2GIS API", validation_alias="DGIS_API_KEY")
    search_api_url: str = Field(..., description="URL for 2GIS Search API", validation_alias="DGIS_SEARCH_API_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"


dgis_api_settings = DGISAPISettings()
