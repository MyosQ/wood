from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from backend.api.constants import AbinEndpoints
from backend.core.dependencies import get_api_client
from backend.services.skogsstyrelsen_client import SkogsstyrelsenClient

router = APIRouter(prefix="/api/abin", tags=["abin"])


@router.get("/helalandet")
async def get_helalandet(
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get national browsing inventory summary for all of Sweden.

    Returns either a single object or a list of objects with historical data.
    """
    result = await client.get(AbinEndpoints.HELALANDET)
    return result


@router.get("/helalandet/geometri")
async def get_helalandet_geometri(
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get national browsing inventory summary with WKT geometry.

    Returns either a single object or a list of objects with historical data.
    """
    result = await client.get(AbinEndpoints.HELALANDET_GEOMETRI)
    return result


@router.get("/landsdel/metadata")
async def get_landsdel_metadata(
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> list[dict[str, Any]]:
    """Get metadata for all regions (landsdel).

    Returns available region codes and names.
    """
    result = await client.get(AbinEndpoints.LANDSDEL_METADATA)
    return result


@router.get("/landsdel/{landsdelkod}")
async def get_landsdel(
    landsdelkod: str,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get browsing inventory summary for specific region (landsdel).

    Returns either a single object or a list of objects with historical data.
    """
    result = await client.get(AbinEndpoints.LANDSDEL.format(landsdelkod=landsdelkod))
    return result


@router.get("/landsdel/{landsdelkod}/geometri")
async def get_landsdel_geometri(
    landsdelkod: str,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get browsing inventory summary for region with WKT geometry.

    Returns either a single object or a list of objects with historical data.
    """
    result = await client.get(AbinEndpoints.LANDSDEL_GEOMETRI.format(landsdelkod=landsdelkod))
    return result


@router.get("/landsdel/{landsdelkod}/lan/metadata")
async def get_lan_metadata(
    landsdelkod: str,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> list[dict[str, Any]]:
    """Get metadata for counties (län) in specific region.

    Returns available county codes and names.
    """
    result = await client.get(AbinEndpoints.LAN_METADATA.format(landsdelkod=landsdelkod))
    return result


@router.get("/lan/{lankod}")
async def get_lan(
    lankod: str,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get browsing inventory summary for specific county (län).

    Returns either a single object or a list of objects with historical data.
    """
    result = await client.get(AbinEndpoints.LAN.format(lankod=lankod))
    return result


@router.get("/lan/{lankod}/geometri")
async def get_lan_geometri(
    lankod: str,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get browsing inventory summary for county with WKT geometry.

    Returns either a single object or a list of objects with historical data.
    """
    result = await client.get(AbinEndpoints.LAN_GEOMETRI.format(lankod=lankod))
    return result


@router.get("/landsdel/{landsdelkod}/lan/{lankod}/afo/metadata")
async def get_afo_metadata(
    landsdelkod: str,
    lankod: str,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> list[dict[str, Any]]:
    """Get metadata for moose management areas (ÄFO) in county.

    Returns available ÄFO numbers and names.
    """
    result = await client.get(
        AbinEndpoints.AFO_METADATA.format(landsdelkod=landsdelkod, lankod=lankod)
    )
    return result


@router.get("/lan/{lankod}/afo/{afonr}")
async def get_afo(
    lankod: str,
    afonr: int,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get browsing inventory summary for moose management area (ÄFO).

    Returns either a single object or a list of objects with historical data.
    """
    result = await client.get(AbinEndpoints.AFO.format(lankod=lankod, afonr=afonr))
    return result


@router.get("/lan/{lankod}/afo/{afonr}/geometri")
async def get_afo_geometri(
    lankod: str,
    afonr: int,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get browsing inventory summary for ÄFO with WKT geometry.

    Returns either a single object or a list of objects with historical data.
    """
    result = await client.get(AbinEndpoints.AFO_GEOMETRI.format(lankod=lankod, afonr=afonr))
    return result


@router.get("/landsdel/{landsdelkod}/lan/{lankod}/afo/{afonr}/stratum/metadata")
async def get_stratum_metadata(
    landsdelkod: str,
    lankod: str,
    afonr: int,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> list[dict[str, Any]]:
    """Get metadata for sub-areas (stratum) in ÄFO.

    Returns available stratum numbers.
    """
    result = await client.get(
        AbinEndpoints.STRATUM_METADATA.format(landsdelkod=landsdelkod, lankod=lankod, afonr=afonr)
    )
    return result


@router.get("/lan/{lankod}/afo/{afonr}/stratum/{delomradesnummer}")
async def get_stratum(
    lankod: str,
    afonr: int,
    delomradesnummer: int,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get browsing inventory summary for sub-area (stratum).

    Returns either a single object or a list of objects with historical data.
    """
    result = await client.get(
        AbinEndpoints.STRATUM.format(lankod=lankod, afonr=afonr, delomradesnummer=delomradesnummer)
    )
    return result


@router.get("/lan/{lankod}/afo/{afonr}/stratum/{delomradesnummer}/geometri")
async def get_stratum_geometri(
    lankod: str,
    afonr: int,
    delomradesnummer: int,
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any] | list[dict[str, Any]]:
    """Get browsing inventory summary for stratum with WKT geometry.

    Returns either a single object or a list of objects with historical data.
    """
    result = await client.get(
        AbinEndpoints.STRATUM_GEOMETRI.format(lankod=lankod, afonr=afonr, delomradesnummer=delomradesnummer)
    )
    return result


@router.get("/api-info")
async def get_abin_api_info(
    client: SkogsstyrelsenClient = Depends(get_api_client),
) -> dict[str, Any]:
    """Get ABIN API information and version details."""
    result = await client.get(AbinEndpoints.API_INFO)
    return result
