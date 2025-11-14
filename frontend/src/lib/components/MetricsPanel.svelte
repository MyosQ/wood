<script lang="ts">
  import {
    getBiomassa,
    getVolym,
    getGrundyta,
    getMedelhojd,
    getMedeldiameter,
    getBiomassaHistogram,
    getVolymHistogram,
    getGrundytaHistogram,
    getMedelhojdHistogram,
    getMedeldiameterHistogram,
    type HistogramRequest,
  } from '../services/grunddata';
  import { LAND_TYPES } from '../examples';
  import { ApiException } from '../api';
  import HistogramChart from './HistogramChart.svelte';
  import ProjectionPanel from './ProjectionPanel.svelte';

  interface Props {
    geometri: string;
    name: string;
  }

  let { geometri, name }: Props = $props();

  type Tab = 'metrics' | 'histograms' | 'projection';
  let activeTab = $state<Tab>('metrics');

  let loading = $state(false);
  let histogramsLoading = $state(false);
  let error = $state('');
  let biomassaResult: any = $state(null);
  let volymResult: any = $state(null);
  let grundytaResult: any = $state(null);
  let medelhojdResult: any = $state(null);
  let medeldiameterResult: any = $state(null);

  // Histogram results
  let biomassaHistogram: any = $state(null);
  let volymHistogram: any = $state(null);
  let grundytaHistogram: any = $state(null);
  let medelhojdHistogram: any = $state(null);
  let medeldiameterHistogram: any = $state(null);

  // Fetch metrics when geometri changes
  $effect(() => {
    if (geometri) {
      fetchMetrics();
    }
  });

  // Fetch histograms when tab changes to histograms
  $effect(() => {
    if (geometri && activeTab === 'histograms' && !biomassaHistogram) {
      fetchHistograms();
    }
  });

  async function fetchMetrics() {
    loading = true;
    error = '';
    biomassaResult = null;
    volymResult = null;
    grundytaResult = null;
    medelhojdResult = null;
    medeldiameterResult = null;

    try {
      const requestParams = {
        geometri,
        marktyp: [LAND_TYPES.PRODUCTIVE_FOREST],
        pixelstorlek: 2,
      };

      // Fetch all five metrics in parallel
      const [biomassa, volym, grundyta, medelhojd, medeldiameter] = await Promise.all([
        getBiomassa(requestParams),
        getVolym(requestParams),
        getGrundyta(requestParams),
        getMedelhojd(requestParams),
        getMedeldiameter(requestParams),
      ]);

      biomassaResult = biomassa;
      volymResult = volym;
      grundytaResult = grundyta;
      medelhojdResult = medelhojd;
      medeldiameterResult = medeldiameter;
    } catch (err) {
      if (err instanceof ApiException) {
        error = `${err.errorType}: ${err.message}`;
      } else {
        error = 'Failed to fetch forest metrics';
      }
    } finally {
      loading = false;
    }
  }

  async function fetchHistograms() {
    histogramsLoading = true;
    error = '';

    try {
      const baseParams = {
        geometri,
        marktyp: [LAND_TYPES.PRODUCTIVE_FOREST],
        pixelstorlek: 2,
      };

      // Fetch all five histograms in parallel with metric-specific parameters
      const [biomassa, volym, grundyta, medelhojd, medeldiameter] = await Promise.all([
        getBiomassaHistogram({ ...baseParams, klassBredd: 100, antalKlasser: 20 }),
        getVolymHistogram({ ...baseParams, klassBredd: 50, antalKlasser: 20 }),
        getGrundytaHistogram({ ...baseParams, klassBredd: 5, antalKlasser: 10 }),
        getMedelhojdHistogram({ ...baseParams, klassBredd: 50, antalKlasser: 10 }),
        getMedeldiameterHistogram({ ...baseParams, klassBredd: 5, antalKlasser: 20 }),
      ]);

      biomassaHistogram = biomassa;
      volymHistogram = volym;
      grundytaHistogram = grundyta;
      medelhojdHistogram = medelhojd;
      medeldiameterHistogram = medeldiameter;
    } catch (err) {
      if (err instanceof ApiException) {
        error = `${err.errorType}: ${err.message}`;
      } else {
        error = 'Failed to fetch histograms';
      }
    } finally {
      histogramsLoading = false;
    }
  }

  // Extract histogram data from API response
  function extractHistogramData(response: any): any[] {
    if (!response?.data) return [];
    const landTypeData = Object.values(response.data)[0] as any;
    if (!Array.isArray(landTypeData)) return [];

    // Transform API field names to match HistogramChart component expectations
    return landTypeData.map((item: any) => ({
      klassMin: item.klassMinVarde,
      klassMax: item.klassMaxVarde,
      areal: item.arealHa
    }));
  }
</script>

<div
  class="backdrop-blur-md bg-[var(--glass-bg)] border border-[var(--glass-border)] rounded-lg shadow-glass p-4 max-w-md"
  role="region"
  aria-label="Forest Metrics Panel"
>
  <h2 class="text-lg font-semibold text-text-primary mb-3">{name}</h2>

  <!-- Tab Navigation -->
  <div class="flex gap-1 mb-4 border-b border-[var(--glass-border)]" role="tablist">
    <button
      role="tab"
      aria-selected={activeTab === 'metrics'}
      onclick={() => (activeTab = 'metrics')}
      class="px-3 py-2 text-sm font-medium transition-colors {activeTab === 'metrics'
        ? 'text-primary border-b-2 border-primary'
        : 'text-text-secondary hover:text-text-primary'}"
    >
      Metrics
    </button>
    <button
      role="tab"
      aria-selected={activeTab === 'histograms'}
      onclick={() => (activeTab = 'histograms')}
      class="px-3 py-2 text-sm font-medium transition-colors {activeTab === 'histograms'
        ? 'text-primary border-b-2 border-primary'
        : 'text-text-secondary hover:text-text-primary'}"
    >
      Distribution
    </button>
    <button
      role="tab"
      aria-selected={activeTab === 'projection'}
      onclick={() => (activeTab = 'projection')}
      class="px-3 py-2 text-sm font-medium transition-colors {activeTab === 'projection'
        ? 'text-primary border-b-2 border-primary'
        : 'text-text-secondary hover:text-text-primary'}"
    >
      Projection
    </button>
  </div>

  <!-- Metrics Tab -->
  {#if activeTab === 'metrics'}
    {#if loading}
      <div class="flex items-center justify-center py-8" role="status">
        <div
          class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"
          aria-hidden="true"
        ></div>
        <span class="sr-only">Loading metrics</span>
      </div>
    {/if}

    {#if error}
      <div
        class="rounded-lg border border-error-border bg-error-bg p-3 text-error-text text-sm"
        role="alert"
      >
        {error}
      </div>
    {/if}

    {#if biomassaResult && volymResult && grundytaResult && medelhojdResult && medeldiameterResult && !loading}
    <div class="space-y-4">
      <!-- Biomass -->
      <div class="border-b border-[var(--glass-border)] pb-3">
        <div class="text-sm text-text-secondary mb-2">Biomass</div>
        {#each Object.entries(biomassaResult.data) as [marktyp, data] (marktyp)}
          {#if (data as any).medelvarde !== undefined}
            <div>
              <span class="text-xl font-bold text-primary">
                {(data as any).medelvarde.toFixed(1)}
              </span>
              <span class="text-sm text-text-tertiary ml-1">ton TS/ha</span>
            </div>
            {#if (data as any).arealHa !== undefined}
              <div class="text-xs text-text-tertiary mt-1">
                Area: {(data as any).arealHa.toFixed(2)} ha
              </div>
            {/if}
          {:else}
            <div class="text-sm text-text-tertiary italic">No data available</div>
          {/if}
        {/each}
      </div>

      <!-- Volume -->
      <div class="border-b border-[var(--glass-border)] pb-3">
        <div class="text-sm text-text-secondary mb-2">Timber Volume</div>
        {#each Object.entries(volymResult.data) as [marktyp, data] (marktyp)}
          {#if (data as any).medel !== undefined}
            <div>
              <span class="text-xl font-bold text-primary">
                {(data as any).medel.toFixed(1)}
              </span>
              <span class="text-sm text-text-tertiary ml-1">m³sk/ha</span>
            </div>
          {:else}
            <div class="text-sm text-text-tertiary italic">No data available</div>
          {/if}
        {/each}
      </div>

      <!-- Basal Area -->
      <div class="border-b border-[var(--glass-border)] pb-3">
        <div class="text-sm text-text-secondary mb-2">Basal Area</div>
        {#each Object.entries(grundytaResult.data) as [marktyp, data] (marktyp)}
          {#if (data as any).medelvarde !== undefined || (data as any).medel !== undefined}
            <div>
              <span class="text-xl font-bold text-primary">
                {((data as any).medelvarde || (data as any).medel).toFixed(1)}
              </span>
              <span class="text-sm text-text-tertiary ml-1">m²/ha</span>
            </div>
          {:else}
            <div class="text-sm text-text-tertiary italic">
              No data available for this land type
            </div>
          {/if}
        {/each}
      </div>

      <!-- Mean Height -->
      <div class="border-b border-[var(--glass-border)] pb-3">
        <div class="text-sm text-text-secondary mb-2">Mean Height</div>
        {#each Object.entries(medelhojdResult.data) as [marktyp, data] (marktyp)}
          {#if (data as any).medelvarde !== undefined || (data as any).medel !== undefined}
            <div>
              <span class="text-xl font-bold text-primary">
                {((data as any).medelvarde || (data as any).medel).toFixed(1)}
              </span>
              <span class="text-sm text-text-tertiary ml-1">m</span>
            </div>
          {:else}
            <div class="text-sm text-text-tertiary italic">
              No data available for this land type
            </div>
          {/if}
        {/each}
      </div>

      <!-- Mean Diameter -->
      <div>
        <div class="text-sm text-text-secondary mb-2">Mean Diameter</div>
        {#each Object.entries(medeldiameterResult.data) as [marktyp, data] (marktyp)}
          {#if (data as any).medelvarde !== undefined || (data as any).medel !== undefined}
            <div>
              <span class="text-xl font-bold text-primary">
                {((data as any).medelvarde || (data as any).medel).toFixed(1)}
              </span>
              <span class="text-sm text-text-tertiary ml-1">cm</span>
            </div>
          {:else}
            <div class="text-sm text-text-tertiary italic">
              No data available for this land type
            </div>
          {/if}
        {/each}
      </div>
    </div>
    {/if}
  {/if}

  <!-- Histograms Tab -->
  {#if activeTab === 'histograms'}
    {#if histogramsLoading}
      <div class="flex items-center justify-center py-8" role="status">
        <div
          class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"
          aria-hidden="true"
        ></div>
        <span class="sr-only">Loading histograms</span>
      </div>
    {/if}

    {#if error}
      <div
        class="rounded-lg border border-error-border bg-error-bg p-3 text-error-text text-sm mb-4"
        role="alert"
      >
        {error}
      </div>
    {/if}

    {#if biomassaHistogram && !histogramsLoading}
      <div class="space-y-4 max-h-[600px] overflow-y-auto">
        <HistogramChart
          metricName="Biomass"
          unit="ton TS/ha"
          data={extractHistogramData(biomassaHistogram)}
        />
        <HistogramChart
          metricName="Timber Volume"
          unit="m³sk/ha"
          data={extractHistogramData(volymHistogram)}
        />
        <HistogramChart
          metricName="Basal Area"
          unit="m²/ha"
          data={extractHistogramData(grundytaHistogram)}
        />
        <HistogramChart
          metricName="Mean Height"
          unit="m"
          data={extractHistogramData(medelhojdHistogram)}
        />
        <HistogramChart
          metricName="Mean Diameter"
          unit="cm"
          data={extractHistogramData(medeldiameterHistogram)}
        />
      </div>
    {/if}
  {/if}

  <!-- Projection Tab -->
  {#if activeTab === 'projection'}
    <ProjectionPanel geometri={geometri} />
  {/if}
</div>
