<script lang="ts">
  import { getBiomassa, getVolym } from '../services/grunddata';
  import { EXAMPLE_SMALL_AREA, LAND_TYPES } from '../examples';
  import { ApiException } from '../api';

  let loading = false;
  let error = '';
  let biomassaResult: any = null;
  let volymResult: any = null;

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

<div class="example-card">
  <h2>Forest Metrics Example</h2>
  <p class="description">
    Calculate biomass and timber volume for a test area near Linköping (~50 hectares).
  </p>

  <button on:click={fetchForestMetrics} disabled={loading} class="fetch-btn">
    {loading ? 'Loading...' : 'Fetch Forest Metrics'}
  </button>

  {#if error}
    <div class="error-box">{error}</div>
  {/if}

  {#if biomassaResult}
    <div class="result-section">
      <h3>Biomass Results</h3>
      {#each Object.entries(biomassaResult.data) as [marktyp, data]}
        <div class="metric">
          <strong>{marktyp}:</strong>
          <span>{data.medelvarde?.toFixed(1)} ton TS/ha</span>
          <span class="light">({data.arealHa?.toFixed(2)} ha)</span>
        </div>
      {/each}
    </div>
  {/if}

  {#if volymResult}
    <div class="result-section">
      <h3>Volume Results</h3>
      {#each Object.entries(volymResult.data) as [marktyp, data]}
        <div class="metric">
          <strong>{marktyp}:</strong>
          <span>{data.medel?.toFixed(1)} m³sk/ha</span>
          <span class="light">({data.arealHa?.toFixed(2)} ha)</span>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .example-card {
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .example-card h2 {
    margin-top: 0;
    color: #2c5f2d;
    font-size: 1.3rem;
  }

  .description {
    color: #666;
    margin-bottom: 1rem;
  }

  .fetch-btn {
    background-color: #2c5f2d;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
  }

  .fetch-btn:hover:not(:disabled) {
    background-color: #1e4620;
  }

  .fetch-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .error-box {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 4px;
    margin-top: 1rem;
    border: 1px solid #f5c6cb;
  }

  .result-section {
    margin-top: 1.5rem;
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 4px;
  }

  .result-section h3 {
    margin-top: 0;
    color: #333;
    font-size: 1.1rem;
  }

  .metric {
    padding: 0.5rem 0;
    border-bottom: 1px solid #e0e0e0;
  }

  .metric:last-child {
    border-bottom: none;
  }

  .metric strong {
    display: inline-block;
    min-width: 200px;
    color: #333;
  }

  .metric span {
    margin-left: 1rem;
    color: #2c5f2d;
    font-weight: 600;
  }

  .light {
    color: #999 !important;
    font-weight: 400 !important;
    font-size: 0.9rem;
  }
</style>
