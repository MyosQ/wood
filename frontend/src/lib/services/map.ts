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
 * Uses distinct, vibrant colors optimized for both light and dark themes.
 * Colors chosen for maximum distinguishability and aesthetic appeal.
 *
 * @param index - Polygon index for color variation
 * @returns LayerStyle configuration for metric polygons
 */
export function getMetricLayerStyle(index: number): LayerStyle {
  // Color palette: vibrant, distinct hues that work in both light/dark modes
  const colorSchemes = [
    { border: '#ff6b6b', fill: '#ff6b6b' }, // Coral Red
    { border: '#4ecdc4', fill: '#4ecdc4' }, // Turquoise
    { border: '#ffe66d', fill: '#ffe66d' }, // Sunny Yellow
    { border: '#a8dadc', fill: '#a8dadc' }, // Sky Blue
    { border: '#f4a261', fill: '#f4a261' }, // Sandy Orange
    { border: '#b4a7d6', fill: '#b4a7d6' }, // Lavender Purple
  ];

  const scheme = colorSchemes[index % colorSchemes.length];

  return {
    color: scheme.border,
    weight: 3,
    fillColor: scheme.fill,
    fillOpacity: 0.35,
    opacity: 1,
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
