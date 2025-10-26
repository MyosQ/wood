/**
 * Example WKT geometries for testing Skogsstyrelsen APIs.
 * All coordinates in SWEREF 99 TM (SRID 3006).
 */

/**
 * Small test area (~50 hectares) near Linköping.
 * Good for quick tests of forest metrics.
 */
export const EXAMPLE_SMALL_AREA =
  'POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))';

/**
 * Medium test area (~200 hectares) in Södermanland.
 * Suitable for histogram calculations.
 */
export const EXAMPLE_MEDIUM_AREA =
  'POLYGON ((633000 6580000, 634500 6580000, 634500 6581500, 633000 6581500, 633000 6580000))';

/**
 * Large test area (~1000 hectares) in Dalarna.
 * Use larger pixel size (10m) for better performance.
 */
export const EXAMPLE_LARGE_AREA =
  'POLYGON ((475000 6750000, 478000 6750000, 478000 6753000, 475000 6753000, 475000 6750000))';

/**
 * Rectangle around Stockholm area for raster/satellite data tests.
 */
export const EXAMPLE_STOCKHOLM =
  'POLYGON ((668000 6580000, 673000 6580000, 673000 6585000, 668000 6585000, 668000 6580000))';

/**
 * Example land type filters for forest statistics.
 */
export const LAND_TYPES = {
  PRODUCTIVE_FOREST: 'ProduktivSkogsmark',
  UNPRODUCTIVE_FOREST: 'ImproduktivSkogsmark',
  ALL_FOREST: 'AllSkogsmark',
  OTHER_LAND: 'OvrigMark',
  ALL_LAND: 'AllMark',
} as const;

/**
 * Example scanning periods (omdrev).
 */
export const SCANNING_PERIODS = {
  PERIOD_1: 1, // 2008-2016
  PERIOD_2: 2, // 2018-2025
  PERIOD_3: 3, // 2025-2032
} as const;

/**
 * Common counties (län) for ABIN API.
 */
export const COUNTIES = {
  STOCKHOLM: '01',
  UPPSALA: '03',
  SODERMANLAND: '04',
  OSTERGOTLAND: '05',
  JONKOPING: '06',
  KRONOBERG: '07',
  KALMAR: '08',
  GOTLAND: '09',
  BLEKINGE: '10',
  SKANE: '12',
  HALLAND: '13',
  VASTRA_GOTALAND: '14',
  VARMLAND: '17',
  OREBRO: '18',
  VASTMANLAND: '19',
  DALARNA: '20',
  GAVLEBORG: '21',
  VASTERNORRLAND: '22',
  JAMTLAND: '23',
  VASTERBOTTEN: '24',
  NORRBOTTEN: '25',
} as const;
