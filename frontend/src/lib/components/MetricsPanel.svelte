<script lang="ts">
  import { getBiomassa, getVolym, getGrundyta } from '../services/grunddata';
  import { LAND_TYPES } from '../examples';
  import { ApiException } from '../api';

  interface Props {
    geometri: string;
    name: string;
  }

  let { geometri, name }: Props = $props();

  let loading = $state(false);
  let error = $state('');
  let biomassaResult: any = $state(null);
  let volymResult: any = $state(null);
  let grundytaResult: any = $state(null);

  // Fetch metrics when geometri changes
  $effect(() => {
    if (geometri) {
      fetchMetrics();
    }
  });

  async function fetchMetrics() {
    loading = true;
    error = '';
    biomassaResult = null;
    volymResult = null;
    grundytaResult = null;

    try {
      const requestParams = {
        geometri,
        marktyp: [LAND_TYPES.PRODUCTIVE_FOREST],
        pixelstorlek: 2,
      };

      // Fetch all three metrics in parallel
      const [biomassa, volym, grundyta] = await Promise.all([
        getBiomassa(requestParams),
        getVolym(requestParams),
        getGrundyta(requestParams),
      ]);

      biomassaResult = biomassa;
      volymResult = volym;
      grundytaResult = grundyta;
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

<div
  class="backdrop-blur-md bg-[var(--glass-bg)] border border-[var(--glass-border)] rounded-lg shadow-lg p-4 max-w-sm"
  style="box-shadow: var(--glass-shadow)"
  role="region"
  aria-label="Forest Metrics Panel"
>
  <h2 class="text-lg font-semibold text-text-primary mb-2">{name}</h2>

  {#if loading}
    <div class="flex items-center justify-center py-8">
      <div
        class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"
        role="status"
        aria-label="Loading metrics"
      ></div>
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

  {#if biomassaResult && volymResult && grundytaResult && !loading}
    <div class="space-y-3">
      <!-- Biomass -->
      <div class="border-b border-[var(--glass-border)] pb-2">
        <div class="text-sm text-text-secondary">Biomass</div>
        {#each Object.entries(biomassaResult.data) as [marktyp, data]}
          <div class="mt-1">
            <span class="text-xl font-bold text-primary">
              {(data as any).medelvarde?.toFixed(1)}
            </span>
            <span class="text-sm text-text-tertiary ml-1">ton TS/ha</span>
          </div>
          <div class="text-xs text-text-tertiary">
            Area: {(data as any).arealHa?.toFixed(2)} ha
          </div>
        {/each}
      </div>

      <!-- Volume -->
      <div class="border-b border-[var(--glass-border)] pb-2">
        <div class="text-sm text-text-secondary">Timber Volume</div>
        {#each Object.entries(volymResult.data) as [marktyp, data]}
          <div class="mt-1">
            <span class="text-xl font-bold text-primary">
              {(data as any).medel?.toFixed(1)}
            </span>
            <span class="text-sm text-text-tertiary ml-1">m³sk/ha</span>
          </div>
        {/each}
      </div>

      <!-- Ground Area -->
      <div class="pb-1">
        <div class="text-sm text-text-secondary">Basal Area</div>
        {#each Object.entries(grundytaResult.data) as [marktyp, data]}
          <div class="mt-1">
            <span class="text-xl font-bold text-primary">
              {(data as any).medelvarde?.toFixed(1)}
            </span>
            <span class="text-sm text-text-tertiary ml-1">m²/ha</span>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>
