<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import * as L from 'leaflet';
  import 'leaflet/dist/leaflet.css';
  import {
    loadGeoJSON,
    getDefaultMapConfig,
    getAdminLayerStyle,
    getMetricLayerStyle,
    styleToPathOptions,
  } from '$lib/services/map';
  import { wktToGeoJSON } from '$lib/utils/coordinates';
  import { EXAMPLE_TINY_POLYGON_1, EXAMPLE_TINY_POLYGON_2 } from '$lib/examples';
  import MetricsPanel from './MetricsPanel.svelte';

  let mapContainer = $state<HTMLDivElement>();
  let map = $state<L.Map | null>(null);
  let loading = $state(true);
  let error = $state('');
  let selectedPolygon = $state<{ geometri: string; name: string } | null>(null);

  // Example polygons with metadata
  const examplePolygons = [
    { wkt: EXAMPLE_TINY_POLYGON_1, name: 'Forest Area 1', index: 0 },
    { wkt: EXAMPLE_TINY_POLYGON_2, name: 'Forest Area 2', index: 1 },
  ];

  onMount(async () => {
    if (!mapContainer) return;

    try {
      // Initialize map
      const config = getDefaultMapConfig();
      map = L.map(mapContainer, {
        center: config.center,
        zoom: config.zoom,
        minZoom: config.minZoom,
        maxZoom: config.maxZoom,
        preferCanvas: true, // Use Canvas renderer for better performance
      });

      // Add OpenStreetMap tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
      }).addTo(map);

      // Load and add Sweden boundary
      const swedenGeoJSON = await loadGeoJSON('geojson/sweden.json');
      const swedenLayer = L.geoJSON(swedenGeoJSON, {
        style: styleToPathOptions({
          color: 'var(--color-primary-dark)',
          weight: 3,
          fillColor: 'var(--color-primary)',
          fillOpacity: 0.05,
          opacity: 0.8,
        }),
      }).addTo(map);

      // Fit map to Sweden bounds
      const bounds = swedenLayer.getBounds();
      map.fitBounds(bounds);

      // Load and add administrative areas
      const adminGeoJSON = await loadGeoJSON('geojson/sweden_administrative_areas.json');
      L.geoJSON(adminGeoJSON, {
        style: styleToPathOptions(getAdminLayerStyle()),
      }).addTo(map);

      // Add example polygons with click handlers
      examplePolygons.forEach(({ wkt, name, index }) => {
        const geojson = wktToGeoJSON(wkt);
        const style = getMetricLayerStyle(index);

        const layer = L.geoJSON(geojson, {
          style: styleToPathOptions(style),
        })
          .addTo(map!)
          .on('click', () => {
            // Update selected polygon
            selectedPolygon = { geometri: wkt, name };

            // Zoom to polygon for better visibility
            const polygonBounds = layer.getBounds();
            map!.flyToBounds(polygonBounds, {
              padding: [50, 50],
              maxZoom: 14,
            });
          });

        // Add tooltip
        layer.bindTooltip(name, {
          permanent: false,
          direction: 'top',
          className: 'custom-tooltip',
        });
      });

      loading = false;
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to initialize map';
      loading = false;
    }
  });

  onDestroy(() => {
    // Clean up map instance to prevent memory leaks
    if (map) {
      map.remove();
      map = null;
    }
  });
</script>

<div class="relative w-screen h-screen">
  <!-- Map Container -->
  <div bind:this={mapContainer} class="w-full h-full" aria-label="Interactive map of Sweden"></div>

  <!-- Loading Overlay -->
  {#if loading}
    <div
      class="absolute top-4 right-4 z-[1000] backdrop-blur-md bg-[var(--glass-bg)] border border-[var(--glass-border)] rounded-lg px-4 py-3 shadow-lg"
      style="box-shadow: var(--glass-shadow)"
      role="status"
      aria-live="polite"
    >
      <div class="flex items-center space-x-3">
        <div
          class="animate-spin rounded-full h-5 w-5 border-b-2 border-primary"
          aria-hidden="true"
        ></div>
        <span class="text-text-primary font-medium">Loading map...</span>
      </div>
    </div>
  {/if}

  <!-- Error Overlay -->
  {#if error}
    <div
      class="absolute top-4 right-4 z-[1000] backdrop-blur-md bg-[var(--glass-bg)] border border-error-border rounded-lg p-4 shadow-lg max-w-md"
      style="box-shadow: var(--glass-shadow)"
      role="alert"
    >
      <h3 class="text-error-text font-semibold mb-2">Error Loading Map</h3>
      <p class="text-text-secondary text-sm">{error}</p>
    </div>
  {/if}

  <!-- Metrics Panel Overlay (bottom-right) -->
  {#if selectedPolygon && !loading}
    <div class="absolute bottom-4 right-4 z-[1000]">
      <MetricsPanel geometri={selectedPolygon.geometri} name={selectedPolygon.name} />
    </div>
  {/if}

  <!-- Instructions Overlay (top-left) -->
  {#if !loading && !error}
    <div
      class="absolute top-4 left-4 z-[1000] backdrop-blur-md bg-[var(--glass-bg)] border border-[var(--glass-border)] rounded-lg px-4 py-3 shadow-lg max-w-xs"
      style="box-shadow: var(--glass-shadow)"
    >
      <h3 class="text-text-primary font-semibold mb-1">Forest Metrics Explorer</h3>
      <p class="text-text-secondary text-sm">
        Click on colored polygons to view forest metrics
      </p>
    </div>
  {/if}
</div>

<style>
  :global(.custom-tooltip) {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(8px);
    color: var(--color-text-primary);
    font-weight: 600;
    padding: 4px 8px;
    border-radius: 4px;
    box-shadow: var(--glass-shadow);
  }
</style>
