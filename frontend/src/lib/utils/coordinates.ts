/**
 * Coordinate transformation utilities for converting between
 * SWEREF99 TM (SRID 3006) and WGS84 (SRID 4326).
 */

import proj4 from 'proj4';

// Define SWEREF99 TM projection (EPSG:3006)
const SWEREF99_TM =
  '+proj=utm +zone=33 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs +type=crs';

// WGS84 is built into proj4 as 'EPSG:4326'
const WGS84 = 'EPSG:4326';

/**
 * Convert WGS84 coordinates (lon, lat) to SWEREF99 TM (easting, northing).
 *
 * @param lon - Longitude in decimal degrees
 * @param lat - Latitude in decimal degrees
 * @returns [easting, northing] in meters (SWEREF99 TM)
 *
 * @example
 * // Stockholm coordinates
 * const [easting, northing] = wgs84ToSweref99(18.0686, 59.3293);
 * // Returns approximately [674032, 6580822]
 */
export function wgs84ToSweref99(lon: number, lat: number): [number, number] {
  return proj4(WGS84, SWEREF99_TM, [lon, lat]) as [number, number];
}

/**
 * Convert SWEREF99 TM coordinates (easting, northing) to WGS84 (lon, lat).
 *
 * @param easting - Easting coordinate in meters
 * @param northing - Northing coordinate in meters
 * @returns [lon, lat] in decimal degrees (WGS84)
 *
 * @example
 * const [lon, lat] = sweref99ToWgs84(674032, 6580822);
 * // Returns approximately [18.0686, 59.3293] (Stockholm)
 */
export function sweref99ToWgs84(easting: number, northing: number): [number, number] {
  return proj4(SWEREF99_TM, WGS84, [easting, northing]) as [number, number];
}

/**
 * Parse WKT POLYGON string and convert coordinates from SWEREF99 TM to WGS84.
 *
 * @param wkt - WKT POLYGON or MULTIPOLYGON string in SWEREF99 TM
 * @returns GeoJSON Polygon or MultiPolygon feature in WGS84
 *
 * @example
 * const wkt = 'POLYGON ((485486 7018193, 486179 7018193, 486179 7018896, 485486 7018896, 485486 7018193))';
 * const geojson = wktToGeoJSON(wkt);
 */
export function wktToGeoJSON(wkt: string): GeoJSON.Feature<GeoJSON.Polygon | GeoJSON.MultiPolygon> {
  // Remove POLYGON/MULTIPOLYGON wrapper and parentheses
  const isMulti = wkt.trim().toUpperCase().startsWith('MULTIPOLYGON');
  let coordStr = wkt
    .replace(/^(MULTI)?POLYGON\s*\(\s*/i, '')
    .replace(/\s*\)\s*$/, '');

  const parseRing = (ringStr: string): [number, number][] => {
    return ringStr
      .replace(/^\(\s*/, '')
      .replace(/\s*\)$/, '')
      .split(',')
      .map(pair => {
        const [easting, northing] = pair.trim().split(/\s+/).map(Number);
        return sweref99ToWgs84(easting, northing);
      });
  };

  if (isMulti) {
    // MULTIPOLYGON (((x y, ...)), ((x y, ...)))
    const polygons = coordStr.match(/\(\([^)]+\)\)/g) || [];
    const coordinates = polygons.map(polyStr => {
      const rings = polyStr.match(/\([^)]+\)/g) || [];
      return rings.map(parseRing);
    });

    return {
      type: 'Feature',
      geometry: {
        type: 'MultiPolygon',
        coordinates,
      },
      properties: {},
    };
  } else {
    // POLYGON ((x y, ...))
    const rings = coordStr.match(/\([^)]+\)/g) || [];
    const coordinates = rings.map(parseRing);

    return {
      type: 'Feature',
      geometry: {
        type: 'Polygon',
        coordinates,
      },
      properties: {},
    };
  }
}

/**
 * Convert GeoJSON Polygon/MultiPolygon from WGS84 to WKT in SWEREF99 TM.
 * Used for sending geometries to Skogsstyrelsen APIs.
 *
 * @param geojson - GeoJSON feature in WGS84
 * @returns WKT POLYGON or MULTIPOLYGON string in SWEREF99 TM
 */
export function geojsonToWKT(
  geojson: GeoJSON.Feature<GeoJSON.Polygon | GeoJSON.MultiPolygon>
): string {
  const { geometry } = geojson;

  const formatRing = (ring: GeoJSON.Position[]): string => {
    const coords = ring
      .map(pos => {
        const [lon, lat] = pos;
        const [easting, northing] = wgs84ToSweref99(lon, lat);
        return `${easting} ${northing}`;
      })
      .join(', ');
    return `(${coords})`;
  };

  if (geometry.type === 'MultiPolygon') {
    const polygons = geometry.coordinates
      .map(poly => {
        const rings = poly.map(formatRing).join(', ');
        return `(${rings})`;
      })
      .join(', ');
    return `MULTIPOLYGON (${polygons})`;
  } else {
    const rings = geometry.coordinates.map(formatRing).join(', ');
    return `POLYGON (${rings})`;
  }
}
