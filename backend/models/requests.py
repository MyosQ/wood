from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BaseAPIRequest(BaseModel):
    """Base class for API request models with common serialization."""

    def to_api_dict(self) -> dict[str, Any]:
        """Convert to API-compatible dictionary with aliases and excluding None values."""
        return self.model_dump(by_alias=True, exclude_none=True)


class SclHistogramDateSummaryRequest(BaseAPIRequest):
    """Request model for SCL histogram date summary."""

    model_config = ConfigDict(populate_by_name=True)

    min_datum: str | None = Field(None, alias="minDatum", description="Start date (ISO 8601)")
    max_datum: str | None = Field(None, alias="maxDatum", description="End date (ISO 8601)")
    min_tackning_indexruta: float | None = Field(
        None,
        alias="minTackningIndexruta",
        ge=0.0,
        le=1.0,
        description="Minimum grid coverage (0.0-1.0)",
    )
    min_anvandbar_data: float | None = Field(
        None,
        alias="minAnvandbarData",
        ge=0.0,
        lt=1.0,
        description="Minimum usable data quality (0.0-0.99)",
    )
    extent: str = Field(..., description="WKT polygon in SWEREF 99 TM")


class SclHistogramByBkidRequest(BaseAPIRequest):
    """Request model for SCL histogram by grid ID."""

    model_config = ConfigDict(populate_by_name=True)

    min_datum: str = Field(..., alias="minDatum", description="Start date")
    max_datum: str = Field(..., alias="maxDatum", description="End date")
    min_tackning_indexruta: float | None = Field(
        None, alias="minTackningIndexruta", ge=0.0, le=1.0
    )
    bk_id: str = Field(..., alias="bkId", description="5km grid ID (e.g., '701_48_50')")
    min_bra_data: float | None = Field(None, alias="minBraData", ge=0.0, lt=1.0)


class StatistikParameters(BaseAPIRequest):
    """Base parameters for forest statistics endpoints."""

    geometri: str = Field(..., description="WKT polygon in SWEREF 99 TM")
    omdrev: int | None = Field(None, ge=1, le=3, description="Scanning period (1-3)")
    pixelstorlek: int | None = Field(
        None, ge=2, le=500, description="Pixel size in meters"
    )
    marktyp: list[str] | None = Field(
        None,
        description="Land types (ProduktivSkogsmark, ImproduktivSkogsmark, AllSkogsmark, OvrigMark, AllMark)",
    )


class HistogramParameters(StatistikParameters):
    """Parameters for histogram endpoints."""

    model_config = ConfigDict(populate_by_name=True)

    klass_bredd: int | None = Field(None, alias="klassBredd", ge=1)
    antal_klasser: int | None = Field(None, alias="antalKlasser", ge=1, le=255)


class FramskrivningVolymParameters(StatistikParameters):
    """Parameters for volume projection endpoint."""

    datum: str | None = Field(None, description="Projection date (YYYY-01-01)")
