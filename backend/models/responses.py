from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ApiInfoResponse(BaseModel):
    """API information response."""

    model_config = ConfigDict(populate_by_name=True)

    api_name: str = Field(alias="apiName")
    api_version: str = Field(alias="apiVersion")
    api_released: str = Field(alias="apiReleased")
    api_documentation: str = Field(alias="apiDocumentation")
    api_status: str = Field(alias="apiStatus")


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str
    status_code: int | None = None
