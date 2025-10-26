from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from backend.api.constants import RasterEndpoints
from backend.core.dependencies import get_api_client
from backend.models.requests import (
    SclHistogramByBkidRequest,
    SclHistogramDateSummaryRequest,
)
from backend.models.responses import ApiInfoResponse
from backend.services.skogsstyrelsen_client import SkogsstyrelsenClient

router = APIRouter(prefix="/api/raster", tags=["raster"])


@router.post("/scl/histogram-date-summary")
async def get_scl_histogram_date_summary(
    request: SclHistogramDateSummaryRequest,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Get Sentinel-2 SCL histogram date summary.

    Find available dates with quality metrics for specified area and time range.
    """
    result = await client.post(
        RasterEndpoints.SCL_HISTOGRAM_DATE_SUMMARY,
        json_data=request.to_api_dict(),
    )
    return result


@router.post("/scl/histogram-by-bkid")
async def get_scl_histogram_by_bkid(
    request: SclHistogramByBkidRequest,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Get SCL histogram for specific 5km index grid.

    Returns Scene Classification Layer histogram for a Lantmäteriet 5km grid cell.
    """
    result = await client.post(
        RasterEndpoints.SCL_HISTOGRAM_BY_BKID,
        json_data=request.to_api_dict(),
    )
    return result


@router.get("/api-info", response_model=ApiInfoResponse)
async def get_raster_api_info(
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Get Raster API information and version details."""
    result = await client.get(RasterEndpoints.API_INFO)
    return result
