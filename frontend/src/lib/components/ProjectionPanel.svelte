<script lang="ts">
  import { onMount } from 'svelte';
  import {
    getVolym,
    getGrundyta,
    getMedelhojd,
    getVolymFramskriven,
    getValidProjectionDates,
    type StatistikRequest,
    type FramskrivningRequest,
  } from '../services/grunddata';
  import { LAND_TYPES } from '../examples';
  import { ApiException } from '../api';

  interface Props {
    geometri: string;
  }

  let { geometri }: Props = $props();

  let loading = $state(false);
  let error = $state('');
  let validDates = $state<string[]>([]);
  let selectedDate = $state('');

  // Current metrics
  let currentVolym = $state<number | null>(null);
  let currentGrundyta = $state<number | null>(null);
  let currentMedelhojd = $state<number | null>(null);

  // Projected metrics
  let projectedVolym = $state<number | null>(null);
  let projectedGrundyta = $state<number | null>(null);
  let projectedMedelhojd = $state<number | null>(null);

  // Load valid dates on mount
  onMount(async () => {
    try {
      validDates = await getValidProjectionDates();
      if (validDates.length > 0) {
        selectedDate = validDates[0];
      }
    } catch (err) {
      error = 'Failed to load projection dates';
    }
  });

  // Fetch current metrics when geometri changes
  $effect(() => {
    if (geometri) {
      fetchCurrentMetrics();
    }
  });

  // Fetch projection when date or geometri changes
  $effect(() => {
    if (geometri && selectedDate) {
      fetchProjection();
    }
  });

  async function fetchCurrentMetrics() {
    const requestParams: StatistikRequest = {
      geometri,
      marktyp: [LAND_TYPES.PRODUCTIVE_FOREST],
      pixelstorlek: 2,
    };

    try {
      const [volym, grundyta, medelhojd] = await Promise.all([
        getVolym(requestParams),
        getGrundyta(requestParams),
        getMedelhojd(requestParams),
      ]);

      currentVolym = extractMetricValue(volym);
      currentGrundyta = extractMetricValue(grundyta);
      currentMedelhojd = extractMetricValue(medelhojd);
    } catch (err) {
      if (err instanceof ApiException) {
        error = `${err.errorType}: ${err.message}`;
      } else {
        error = 'Failed to fetch current metrics';
      }
    }
  }

  async function fetchProjection() {
    loading = true;
    error = '';

    const requestParams: FramskrivningRequest = {
      geometri,
      marktyp: [LAND_TYPES.PRODUCTIVE_FOREST],
      pixelstorlek: 2,
      datum: selectedDate,
    };

    try {
      const projection = await getVolymFramskriven(requestParams);

      // Extract projected values
      projectedVolym = extractMetricValue(projection, 'volym');
      projectedGrundyta = extractMetricValue(projection, 'grundyta');
      projectedMedelhojd = extractMetricValue(projection, 'medelhojd');
    } catch (err) {
      if (err instanceof ApiException) {
        error = `${err.errorType}: ${err.message}`;
      } else {
        error = 'Failed to fetch projection';
      }
    } finally {
      loading = false;
    }
  }

  // Extract metric value from API response
  function extractMetricValue(response: any, key?: string): number | null {
    if (!response) return null;

    // For VolymFramskriven: top-level keys (volym, grundyta, medelhojd)
    // For regular metrics: nested in .data
    const metricData = key ? response[key] : response?.data;
    if (!metricData) return null;

    // Get first marktyp entry
    const landTypeData = Object.values(metricData)[0] as any;
    if (!landTypeData) return null;

    // Try both field name variations
    return landTypeData?.medelvarde ?? landTypeData?.medel ?? null;
  }

  // Calculate growth percentage
  function calculateGrowth(current: number | null, projected: number | null): number | null {
    if (current === null || projected === null || current === 0) return null;
    return ((projected - current) / current) * 100;
  }

  // Format growth indicator
  function formatGrowth(growth: number | null): string {
    if (growth === null) return '';
    const sign = growth > 0 ? '+' : '';
    return `${sign}${growth.toFixed(1)}%`;
  }

  // Get growth indicator color class
  function getGrowthColor(growth: number | null): string {
    if (growth === null) return 'text-text-tertiary';
    if (growth > 0) return 'text-green-500';
    if (growth < 0) return 'text-red-500';
    return 'text-text-tertiary';
  }
</script>

<div
  class="backdrop-blur-md bg-[var(--glass-bg)] border border-[var(--glass-border)] rounded-lg shadow-glass p-4"
  role="region"
  aria-label="Forest Growth Projection"
>
  <h3 class="text-sm font-semibold text-text-primary mb-3">Growth Projection</h3>

  <!-- Date Picker -->
  <div class="mb-4">
    <label for="projection-date" class="block text-xs text-text-secondary mb-1">
      Project to date
    </label>
    <select
      id="projection-date"
      bind:value={selectedDate}
      class="w-full px-3 py-2 rounded bg-[var(--color-surface)] border border-[var(--glass-border)] text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-primary"
    >
      {#each validDates as date (date)}
        <option value={date}>{date}</option>
      {/each}
    </select>
  </div>

  {#if loading}
    <div class="flex items-center justify-center py-8" role="status">
      <div
        class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"
        aria-hidden="true"
      ></div>
      <span class="sr-only">Loading projection</span>
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

  {#if currentVolym !== null && projectedVolym !== null && !loading}
    <div class="space-y-3">
      <!-- Volume -->
      <div class="border-b border-[var(--glass-border)] pb-3">
        <div class="text-xs text-text-secondary mb-2">Timber Volume</div>
        <div class="flex items-baseline gap-2">
          <span class="text-lg font-bold text-text-primary">
            {currentVolym.toFixed(1)}
          </span>
          <span class="text-primary text-lg">→</span>
          <span class="text-lg font-bold text-primary">
            {projectedVolym.toFixed(1)}
          </span>
          <span class="text-xs text-text-tertiary">m³sk/ha</span>
          <span class="text-xs ml-auto {getGrowthColor(calculateGrowth(currentVolym, projectedVolym))}">
            {formatGrowth(calculateGrowth(currentVolym, projectedVolym))}
          </span>
        </div>
      </div>

      <!-- Basal Area -->
      <div class="border-b border-[var(--glass-border)] pb-3">
        <div class="text-xs text-text-secondary mb-2">Basal Area</div>
        <div class="flex items-baseline gap-2">
          <span class="text-lg font-bold text-text-primary">
            {currentGrundyta?.toFixed(1) ?? 'N/A'}
          </span>
          <span class="text-primary text-lg">→</span>
          <span class="text-lg font-bold text-primary">
            {projectedGrundyta?.toFixed(1) ?? 'N/A'}
          </span>
          <span class="text-xs text-text-tertiary">m²/ha</span>
          <span class="text-xs ml-auto {getGrowthColor(calculateGrowth(currentGrundyta, projectedGrundyta))}">
            {formatGrowth(calculateGrowth(currentGrundyta, projectedGrundyta))}
          </span>
        </div>
      </div>

      <!-- Mean Height -->
      <div>
        <div class="text-xs text-text-secondary mb-2">Mean Height</div>
        <div class="flex items-baseline gap-2">
          <span class="text-lg font-bold text-text-primary">
            {currentMedelhojd?.toFixed(1) ?? 'N/A'}
          </span>
          <span class="text-primary text-lg">→</span>
          <span class="text-lg font-bold text-primary">
            {projectedMedelhojd?.toFixed(1) ?? 'N/A'}
          </span>
          <span class="text-xs text-text-tertiary">m</span>
          <span class="text-xs ml-auto {getGrowthColor(calculateGrowth(currentMedelhojd, projectedMedelhojd))}">
            {formatGrowth(calculateGrowth(currentMedelhojd, projectedMedelhojd))}
          </span>
        </div>
      </div>
    </div>
  {/if}
</div>
