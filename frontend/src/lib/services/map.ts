/**
 * Map service layer for Leaflet map configuration and GeoJSON loading.
 */

import type * as L from 'leaflet';

/**
 * Map configuration settings.
 */
export interface MapConfig {
  center: [number, number]; // [lat, lon]
  zoom: number;
  minZoom?: number;
  maxZoom?: number;
}

/**
 * Leaflet layer styling configuration.
 */
export interface LayerStyle {
  color?: string;
  weight?: number;
  fillColor?: string;
  fillOpacity?: number;
  opacity?: number;
}

/**
 * Get default map configuration centered on Sweden.
 *
 * @returns MapConfig with Sweden-centered settings
 */
export function getDefaultMapConfig(): MapConfig {
  return {
    center: [62.0, 15.0], // Center of Sweden
    zoom: 5,
    minZoom: 4,
    maxZoom: 18,
  };
}

/**
 * Get styling for administrative area layers.
 * Uses CSS variables for theme compatibility.
 *
 * @returns LayerStyle configuration for admin boundaries
 */
export function getAdminLayerStyle(): LayerStyle {
  return {
    color: 'var(--color-primary)',
    weight: 2,
    fillColor: 'var(--color-primary-light)',
    fillOpacity: 0.1,
    opacity: 0.6,
  };
}

/**
 * Get styling for forestry metric polygons.
 * Uses bright colors for easy visibility during testing.
 *
 * @param index - Polygon index for color variation
 * @returns LayerStyle configuration for metric polygons
 */
export function getMetricLayerStyle(index: number): LayerStyle {
  const colors = ['#ff4444', '#00dddd']; // Red, Cyan - easy to spot
  const color = colors[index % colors.length];

  return {
    color: color,
    weight: 3,
    fillColor: color,
    fillOpacity: 0.3,
    opacity: 0.9,
  };
}

/**
 * Load GeoJSON file from public directory.
 *
 * @param path - Path relative to public directory (e.g., 'geojson/sweden.json')
 * @returns Promise resolving to GeoJSON FeatureCollection
 *
 * @throws Error if fetch fails or JSON parsing fails
 *
 * @example
 * const sweden = await loadGeoJSON('geojson/sweden.json');
 */
export async function loadGeoJSON(path: string): Promise<GeoJSON.FeatureCollection> {
  const response = await fetch(`/${path}`);

  if (!response.ok) {
    throw new Error(`Failed to load GeoJSON from ${path}: ${response.statusText}`);
  }

  const data = await response.json();
  return data as GeoJSON.FeatureCollection;
}

/**
 * Create a Leaflet path options object from LayerStyle.
 * Converts our simplified style interface to Leaflet's PathOptions.
 *
 * @param style - Our LayerStyle configuration
 * @returns Leaflet PathOptions
 */
export function styleToPathOptions(style: LayerStyle): L.PathOptions {
  return {
    color: style.color,
    weight: style.weight,
    fillColor: style.fillColor,
    fillOpacity: style.fillOpacity,
    opacity: style.opacity,
  };
}
