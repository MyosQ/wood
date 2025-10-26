/**
 * API endpoint constants for all services
 *
 * Centralized definition of all API endpoints to avoid magic strings
 * and make it easier to update URLs.
 */

export const ENDPOINTS = {
  /**
   * Forest base data (Skogliga grunddata) API endpoints
   */
  grunddata: {
    validDates: '/api/grunddata/valid-dates',
    biomassa: '/api/grunddata/biomassa',
    biomassaHistogram: '/api/grunddata/biomassa/histogram',
    volym: '/api/grunddata/volym',
    volymHistogram: '/api/grunddata/volym/histogram',
    volymFramskriven: '/api/grunddata/volym-framskriven',
    grundyta: '/api/grunddata/grundyta',
    grundytaHistogram: '/api/grunddata/grundyta/histogram',
    medelhojd: '/api/grunddata/medelhojd',
    medelhojdHistogram: '/api/grunddata/medelhojd/histogram',
    medeldiameter: '/api/grunddata/medeldiameter',
    medeldiameterHistogram: '/api/grunddata/medeldiameter/histogram',
    apiInfo: '/api/grunddata/api-info',
  },

  /**
   * ABIN (browsing inventory) API endpoints
   */
  abin: {
    helalandet: '/api/abin/helalandet',
    helalandetGeometri: '/api/abin/helalandet/geometri',
    landsdelMetadata: '/api/abin/landsdel/metadata',
    landsdel: (landsdelkod: string) => `/api/abin/landsdel/${landsdelkod}`,
    landsdelGeometri: (landsdelkod: string) => `/api/abin/landsdel/${landsdelkod}/geometri`,
    lanMetadata: (landsdelkod: string) => `/api/abin/landsdel/${landsdelkod}/lan/metadata`,
    lan: (lankod: string) => `/api/abin/lan/${lankod}`,
    lanGeometri: (lankod: string) => `/api/abin/lan/${lankod}/geometri`,
    afoMetadata: (landsdelkod: string, lankod: string) =>
      `/api/abin/landsdel/${landsdelkod}/lan/${lankod}/afo/metadata`,
    afo: (lankod: string, afonr: number) => `/api/abin/lan/${lankod}/afo/${afonr}`,
    afoGeometri: (lankod: string, afonr: number) => `/api/abin/lan/${lankod}/afo/${afonr}/geometri`,
    stratumMetadata: (landsdelkod: string, lankod: string, afonr: number) =>
      `/api/abin/landsdel/${landsdelkod}/lan/${lankod}/afo/${afonr}/stratum/metadata`,
    stratum: (lankod: string, afonr: number, delomradesnummer: number) =>
      `/api/abin/lan/${lankod}/afo/${afonr}/stratum/${delomradesnummer}`,
    stratumGeometri: (lankod: string, afonr: number, delomradesnummer: number) =>
      `/api/abin/lan/${lankod}/afo/${afonr}/stratum/${delomradesnummer}/geometri`,
    apiInfo: '/api/abin/api-info',
  },

  /**
   * Raster (Sentinel-2 satellite data) API endpoints
   */
  raster: {
    sclHistogramDateSummary: '/api/raster/scl/histogram-date-summary',
    sclHistogramByBkid: '/api/raster/scl/histogram-by-bkid',
    apiInfo: '/api/raster/api-info',
  },
} as const;
