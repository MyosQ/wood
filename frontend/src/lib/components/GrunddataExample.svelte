<script lang="ts">
  import { getBiomassa, getVolym } from '../services/grunddata';
  import { EXAMPLE_SMALL_AREA, LAND_TYPES } from '../examples';
  import { ApiException } from '../api';

  let loading = $state(false);
  let error = $state('');
  let biomassaResult: any = $state(null);
  let volymResult: any = $state(null);

  async function fetchForestMetrics() {
    loading = true;
    error = '';
    biomassaResult = null;
    volymResult = null;

    try {
      const requestParams = {
        geometri: EXAMPLE_SMALL_AREA,
        marktyp: [LAND_TYPES.PRODUCTIVE_FOREST],
        pixelstorlek: 2,
      };

      // Fetch both biomass and volume in parallel
      const [biomassa, volym] = await Promise.all([
        getBiomassa(requestParams),
        getVolym(requestParams),
      ]);

      biomassaResult = biomassa;
      volymResult = volym;
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
</script>

<div class="rounded-lg border border-border bg-surface p-6 shadow-md">
  <h2 class="text-xl font-semibold text-primary">Forest Metrics Example</h2>
  <p class="mt-2 text-text-secondary">
    Calculate biomass and timber volume for a test area near Linköping (~50 hectares).
  </p>

  <button
    onclick={fetchForestMetrics}
    disabled={loading}
    class="mt-4 rounded-lg bg-primary px-6 py-3 font-medium text-white transition-colors hover:bg-primary-dark focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:bg-primary"
  >
    {loading ? 'Loading...' : 'Fetch Forest Metrics'}
  </button>

  {#if error}
    <div class="mt-4 rounded-lg border border-error-border bg-error-bg p-4 text-error-text">
      {error}
    </div>
  {/if}

  {#if biomassaResult}
    <div class="mt-6 rounded-lg bg-background p-4 border border-border">
      <h3 class="mb-3 text-lg font-medium text-text-primary">Biomass Results</h3>
      {#each Object.entries(biomassaResult.data) as [marktyp, data]}
        <div class="border-b border-border py-3 last:border-0">
          <span class="font-semibold text-text-primary">{marktyp}:</span>
          <span class="ml-4 font-semibold text-primary">
            {(data as any).medelvarde?.toFixed(1)} ton TS/ha
          </span>
          <span class="ml-2 text-sm text-text-tertiary">
            ({(data as any).arealHa?.toFixed(2)} ha)
          </span>
        </div>
      {/each}
    </div>
  {/if}

  {#if volymResult}
    <div class="mt-6 rounded-lg bg-background p-4 border border-border">
      <h3 class="mb-3 text-lg font-medium text-text-primary">Volume Results</h3>
      {#each Object.entries(volymResult.data) as [marktyp, data]}
        <div class="border-b border-border py-3 last:border-0">
          <span class="font-semibold text-text-primary">{marktyp}:</span>
          <span class="ml-4 font-semibold text-primary">
            {(data as any).medel?.toFixed(1)} m³sk/ha
          </span>
          <span class="ml-2 text-sm text-text-tertiary">
            ({(data as any).arealHa?.toFixed(2)} ha)
          </span>
        </div>
      {/each}
    </div>
  {/if}
</div>
