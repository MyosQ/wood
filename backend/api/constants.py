"""API endpoint constants for Skogsstyrelsen APIs."""

from __future__ import annotations


class RasterEndpoints:
    """Raster API (Sentinel-2 satellite data) endpoint paths."""

    SCL_HISTOGRAM_DATE_SUMMARY = "/raster/v1/scl/histogramdatesummary"
    SCL_HISTOGRAM_BY_BKID = "/raster/v1/SclHistogramByBkid"
    API_INFO = "/raster/v1/api-info"


class GrundataEndpoints:
    """Forest base data (Skogliga grunddata) API endpoint paths."""

    VALID_DATES = "/skogligagrunddata/v1/VolymFramskriven/GiltigaDatum"
    BIOMASSA = "/skogligagrunddata/v1/Biomassa"
    BIOMASSA_HISTOGRAM = "/skogligagrunddata/v1/Biomassa/Histogram"
    VOLYM = "/skogligagrunddata/v1/Volym"
    VOLYM_HISTOGRAM = "/skogligagrunddata/v1/Volym/Histogram"
    VOLYM_FRAMSKRIVEN = "/skogligagrunddata/v1/VolymFramskriven"
    GRUNDYTA = "/skogligagrunddata/v1/Grundyta"
    GRUNDYTA_HISTOGRAM = "/skogligagrunddata/v1/Grundyta/Histogram"
    MEDELHOJD = "/skogligagrunddata/v1/Medelhojd"
    MEDELHOJD_HISTOGRAM = "/skogligagrunddata/v1/Medelhojd/Histogram"
    MEDELDIAMETER = "/skogligagrunddata/v1/Medeldiameter"
    MEDELDIAMETER_HISTOGRAM = "/skogligagrunddata/v1/Medeldiameter/Histogram"
    API_INFO = "/skogligagrunddata/v1/api-info"


class AbinEndpoints:
    """ABIN (browsing inventory) API endpoint paths."""

    HELALANDET = "/abin/v2/helalandet"
    HELALANDET_GEOMETRI = "/abin/v2/helalandet/geometri"
    LANDSDEL_METADATA = "/abin/v2/landsdel/metadata"
    LANDSDEL = "/abin/v2/landsdel/{landsdelkod}"
    LANDSDEL_GEOMETRI = "/abin/v2/landsdel/{landsdelkod}/geometri"
    LAN_METADATA = "/abin/v2/landsdel/{landsdelkod}/lan/metadata"
    LAN = "/abin/v2/lan/{lankod}"
    LAN_GEOMETRI = "/abin/v2/lan/{lankod}/geometri"
    AFO_METADATA = "/abin/v2/landsdel/{landsdelkod}/lan/{lankod}/afo/metadata"
    AFO = "/abin/v2/lan/{lankod}/afo/{afonr}"
    AFO_GEOMETRI = "/abin/v2/lan/{lankod}/afo/{afonr}/geometri"
    STRATUM_METADATA = "/abin/v2/landsdel/{landsdelkod}/lan/{lankod}/afo/{afonr}/stratum/metadata"
    STRATUM = "/abin/v2/lan/{lankod}/afo/{afonr}/stratum/{delomradesnummer}"
    STRATUM_GEOMETRI = "/abin/v2/lan/{lankod}/afo/{afonr}/stratum/{delomradesnummer}/geometri"
    API_INFO = "/abin/v2/api-info"
