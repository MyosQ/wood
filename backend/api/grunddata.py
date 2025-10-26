from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from backend.api.constants import GrundataEndpoints
from backend.core.dependencies import get_api_client
from backend.models.requests import (
    FramskrivningVolymParameters,
    HistogramParameters,
    StatistikParameters,
)
from backend.services.skogsstyrelsen_client import SkogsstyrelsenClient

router = APIRouter(prefix="/api/grunddata", tags=["grunddata"])


@router.get("/valid-dates")
async def get_valid_projection_dates(
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> list[str]:
    """Get valid dates for volume projection.

    Returns list of dates in YYYY-MM-DD format (always January 1st).
    """
    result = await client.get(GrundataEndpoints.VALID_DATES)
    return result


@router.post("/biomassa")
async def get_biomassa(
    request: StatistikParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Calculate biomass (ton dry substance/ha) for specified area.

    Returns mean biomass per hectare and total biomass by land type.
    """
    result = await client.post(
        GrundataEndpoints.BIOMASSA,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/biomassa/histogram")
async def get_biomassa_histogram(
    request: HistogramParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Get area distribution across biomass classes.

    Returns area (hectares) per biomass class with configurable class width.
    """
    result = await client.post(
        GrundataEndpoints.BIOMASSA_HISTOGRAM,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/volym")
async def get_volym(
    request: StatistikParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Calculate timber volume (m³sk/ha) for specified area.

    Returns mean volume per hectare and total volume by land type.
    """
    result = await client.post(
        GrundataEndpoints.VOLYM,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/volym/histogram")
async def get_volym_histogram(
    request: HistogramParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Get area distribution across volume classes.

    Returns area (hectares) per volume class with configurable class width.
    """
    result = await client.post(
        GrundataEndpoints.VOLYM_HISTOGRAM,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/volym-framskriven")
async def get_volym_framskriven(
    request: FramskrivningVolymParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Calculate projected volume with growth model.

    Projects volume, mean height, and basal area to specified future date.
    Use /valid-dates to get available projection dates.
    """
    result = await client.post(
        GrundataEndpoints.VOLYM_FRAMSKRIVEN,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/grundyta")
async def get_grundyta(
    request: StatistikParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Calculate basal area (m²/ha) for specified area.

    Returns mean basal area per hectare by land type.
    """
    result = await client.post(
        GrundataEndpoints.GRUNDYTA,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/grundyta/histogram")
async def get_grundyta_histogram(
    request: HistogramParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Get area distribution across basal area classes.

    Returns area (hectares) per basal area class with configurable class width.
    """
    result = await client.post(
        GrundataEndpoints.GRUNDYTA_HISTOGRAM,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/medelhojd")
async def get_medelhojd(
    request: StatistikParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Calculate mean height (meters, basal area weighted) for specified area.

    Returns mean height per hectare by land type.
    """
    result = await client.post(
        GrundataEndpoints.MEDELHOJD,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/medelhojd/histogram")
async def get_medelhojd_histogram(
    request: HistogramParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Get area distribution across height classes.

    Returns area (hectares) per height class with configurable class width.
    """
    result = await client.post(
        GrundataEndpoints.MEDELHOJD_HISTOGRAM,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/medeldiameter")
async def get_medeldiameter(
    request: StatistikParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Calculate mean diameter (cm, basal area weighted) for specified area.

    Returns mean diameter by land type.
    """
    result = await client.post(
        GrundataEndpoints.MEDELDIAMETER,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/medeldiameter/histogram")
async def get_medeldiameter_histogram(
    request: HistogramParameters,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Get area distribution across diameter classes.

    Returns area (hectares) per diameter class with configurable class width.
    """
    result = await client.post(
        GrundataEndpoints.MEDELDIAMETER_HISTOGRAM,
        json_data=request.to_api_dict(),
    )
    return result


@router.get("/api-info")
async def get_grunddata_api_info(
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Get Forest Base Data API information and version details."""
    result = await client.get(GrundataEndpoints.API_INFO)
    return result
