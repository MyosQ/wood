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
  import {
    FOREST_AREA_NORRBOTTEN,
    FOREST_AREA_DALARNA,
    FOREST_AREA_SMALAND,
    FOREST_AREA_VASTRA_GOTALAND,
    FOREST_AREA_GAVLEBORG,
    FOREST_AREA_VASTERBOTTEN,
  } from '$lib/examples';
  import MetricsPanel from './MetricsPanel.svelte';

  // State
  let mapContainer = $state<HTMLDivElement>();
  let map = $state<L.Map | null>(null);
  let loading = $state(true);
  let error = $state('');
  let selectedPolygon = $state<{ geometri: string; name: string } | null>(null);

  // Example forest areas across Sweden
  const FOREST_AREAS = [
    { wkt: FOREST_AREA_NORRBOTTEN, name: 'Norrbotten Forest (1000 ha)', index: 0 },
    { wkt: FOREST_AREA_DALARNA, name: 'Dalarna Forest (800 ha)', index: 1 },
    { wkt: FOREST_AREA_SMALAND, name: 'Småland Forest (600 ha)', index: 2 },
    { wkt: FOREST_AREA_VASTRA_GOTALAND, name: 'Västra Götaland Forest (700 ha)', index: 3 },
    { wkt: FOREST_AREA_GAVLEBORG, name: 'Gävleborg Forest (900 ha)', index: 4 },
    { wkt: FOREST_AREA_VASTERBOTTEN, name: 'Västerbotten Forest (1200 ha)', index: 5 },
  ] as const;

  /**
   * Initialize Leaflet map with base configuration.
   */
  function initializeMap(container: HTMLDivElement): L.Map {
    const config = getDefaultMapConfig();
    return L.map(container, {
      center: config.center,
      zoom: config.zoom,
      minZoom: config.minZoom,
      maxZoom: config.maxZoom,
      preferCanvas: true,
    });
  }

  /**
   * Add OpenStreetMap tile layer to map.
   */
  function addTileLayer(leafletMap: L.Map): void {
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19,
    }).addTo(leafletMap);
  }

  /**
   * Load and add Sweden boundary layer, then fit map to bounds.
   */
  async function addSwedenBoundary(leafletMap: L.Map): Promise<void> {
    const swedenGeoJSON = await loadGeoJSON('geojson/sweden.json');
    const swedenLayer = L.geoJSON(swedenGeoJSON, {
      style: styleToPathOptions({
        color: 'var(--color-primary-dark)',
        weight: 3,
        fillColor: 'var(--color-primary)',
        fillOpacity: 0.05,
        opacity: 0.8,
      }),
    }).addTo(leafletMap);

    const bounds = swedenLayer.getBounds();
    leafletMap.fitBounds(bounds);
  }

  /**
   * Load and add administrative areas layer.
   */
  async function addAdminAreas(leafletMap: L.Map): Promise<void> {
    const adminGeoJSON = await loadGeoJSON('geojson/sweden_administrative_areas.json');
    L.geoJSON(adminGeoJSON, {
      style: styleToPathOptions(getAdminLayerStyle()),
    }).addTo(leafletMap);
  }

  /**
   * Handle polygon click - select and zoom to area.
   */
  function handlePolygonClick(wkt: string, name: string, layer: L.GeoJSON): void {
    selectedPolygon = { geometri: wkt, name };

    const bounds = layer.getBounds();
    map?.flyToBounds(bounds, {
      padding: [50, 50],
      maxZoom: 14,
    });
  }

  /**
   * Create and add forest area polygon layer with interactions.
   */
  function addForestAreaLayer(
    leafletMap: L.Map,
    wkt: string,
    name: string,
    index: number,
  ): void {
    const geojson = wktToGeoJSON(wkt);
    const style = getMetricLayerStyle(index);

    const layer = L.geoJSON(geojson, {
      style: styleToPathOptions(style),
    })
      .addTo(leafletMap)
      .on('click', () => handlePolygonClick(wkt, name, layer));

    layer.bindTooltip(name, {
      permanent: false,
      direction: 'top',
      className: 'custom-tooltip',
    });
  }

  /**
   * Add all forest area polygons to map.
   */
  function addForestAreas(leafletMap: L.Map): void {
    FOREST_AREAS.forEach(({ wkt, name, index }) => {
      addForestAreaLayer(leafletMap, wkt, name, index);
    });
  }

  /**
   * Initialize complete map with all layers.
   */
  async function setupMap(): Promise<void> {
    if (!mapContainer) return;

    try {
      map = initializeMap(mapContainer);
      addTileLayer(map);
      await addSwedenBoundary(map);
      await addAdminAreas(map);
      addForestAreas(map);

      loading = false;
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to initialize map';
      loading = false;
    }
  }

  onMount(() => {
    setupMap();
  });

  onDestroy(() => {
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
      class="absolute top-4 right-4 z-[1000] backdrop-blur-md bg-[var(--glass-bg)] border border-[var(--glass-border)] rounded-lg px-4 py-3 shadow-glass"
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
      class="absolute top-4 right-4 z-[1000] backdrop-blur-md bg-[var(--glass-bg)] border border-error-border rounded-lg p-4 shadow-glass max-w-md"
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
