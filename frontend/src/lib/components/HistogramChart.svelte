<script lang="ts">
  interface HistogramClass {
    klassMin: number;
    klassMax: number;
    areal: number;
  }

  interface Props {
    metricName: string;
    unit: string;
    data: HistogramClass[];
    loading?: boolean;
  }

  let { metricName, unit, data, loading = false }: Props = $props();

  // Calculate max area for scaling bars
  const maxArea = $derived(
    data.length > 0 ? Math.max(...data.map((d) => d.areal)) : 0,
  );

  // Format class label
  function formatClassLabel(min: number, max: number): string {
    return `${min.toFixed(0)}-${max.toFixed(0)}`;
  }

  // Calculate bar height percentage
  function getBarHeight(areal: number): number {
    if (maxArea === 0) return 0;
    return (areal / maxArea) * 100;
  }
</script>

<div
  class="backdrop-blur-md bg-[var(--glass-bg)] border border-[var(--glass-border)] rounded-lg shadow-glass p-4"
  role="region"
  aria-label="{metricName} distribution histogram"
>
  <h3 class="text-sm font-semibold text-text-primary mb-3">
    {metricName} Distribution
  </h3>

  {#if loading}
    <div class="flex items-center justify-center py-8" role="status">
      <div
        class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"
        aria-hidden="true"
      ></div>
      <span class="sr-only">Loading histogram</span>
    </div>
  {:else if data.length === 0}
    <div class="text-sm text-text-tertiary italic py-4">
      No histogram data available
    </div>
  {:else}
    <!-- Chart Container -->
    <div class="space-y-2">
      {#each data as classData, index (index)}
        <div class="flex items-center gap-2">
          <!-- Class Label -->
          <div class="text-xs text-text-secondary w-20 flex-shrink-0 text-right">
            {formatClassLabel(classData.klassMin, classData.klassMax)}
            <span class="text-text-tertiary">{unit}</span>
          </div>

          <!-- Bar Container -->
          <div class="flex-1 h-6 bg-[var(--color-surface)] rounded overflow-hidden">
            <div
              class="h-full bg-primary transition-all duration-300"
              style="width: {getBarHeight(classData.areal)}%"
              role="img"
              aria-label="{classData.areal.toFixed(1)} hectares in range {formatClassLabel(
                classData.klassMin,
                classData.klassMax,
              )} {unit}"
            ></div>
          </div>

          <!-- Area Value -->
          <div class="text-xs text-text-primary w-16 flex-shrink-0">
            {classData.areal.toFixed(1)} ha
          </div>
        </div>
      {/each}
    </div>

    <!-- Legend -->
    <div class="mt-3 pt-3 border-t border-[var(--glass-border)]">
      <div class="text-xs text-text-tertiary">
        Total area: {data.reduce((sum, d) => sum + d.areal, 0).toFixed(1)} ha across {data.length} classes
      </div>
    </div>
  {/if}
</div>
