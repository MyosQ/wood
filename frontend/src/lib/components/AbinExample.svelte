<script lang="ts">
  import { getHelalandet, getLan } from '../services/abin';
  import { COUNTIES } from '../examples';
  import { ApiException } from '../api';

  let loading = false;
  let error = '';
  let nationalResult: any = null;
  let countyResult: any = null;
  let selectedCounty = COUNTIES.STOCKHOLM;

  async function fetchBrowsingData() {
    loading = true;
    error = '';
    nationalResult = null;
    countyResult = null;

    try {
      // Fetch national data and county data in parallel
      const [national, county] = await Promise.all([
        getHelalandet(),
        getLan(selectedCounty),
      ]);

      // Handle both single object and array responses
      // If array, take the most recent (first) entry
      nationalResult = Array.isArray(national) ? national[0] : national;
      countyResult = Array.isArray(county) ? county[0] : county;
    } catch (err) {
      if (err instanceof ApiException) {
        error = `${err.errorType}: ${err.message}`;
      } else {
        error = 'Failed to fetch browsing inventory data';
      }
    } finally {
      loading = false;
    }
  }
</script>

<div class="example-card">
  <h2>Browsing Inventory Example</h2>
  <p class="description">
    View browsing damage statistics from moose and deer inventory (ABIN).
  </p>

  <div class="controls">
    <label>
      County:
      <select bind:value={selectedCounty}>
        <option value={COUNTIES.STOCKHOLM}>Stockholm</option>
        <option value={COUNTIES.UPPSALA}>Uppsala</option>
        <option value={COUNTIES.SODERMANLAND}>Södermanland</option>
        <option value={COUNTIES.OSTERGOTLAND}>Östergötland</option>
        <option value={COUNTIES.JONKOPING}>Jönköping</option>
        <option value={COUNTIES.DALARNA}>Dalarna</option>
        <option value={COUNTIES.VASTERBOTTEN}>Västerbotten</option>
        <option value={COUNTIES.NORRBOTTEN}>Norrbotten</option>
      </select>
    </label>

    <button on:click={fetchBrowsingData} disabled={loading} class="fetch-btn">
      {loading ? 'Loading...' : 'Fetch Browsing Data'}
    </button>
  </div>

  {#if error}
    <div class="error-box">{error}</div>
  {/if}

  {#if nationalResult}
    <div class="result-section">
      <h3>National Summary (Most Recent)</h3>
      <div class="metric">
        <strong>Area:</strong>
        <span>{nationalResult.omrade || 'Hela landet'}</span>
      </div>
      <div class="metric">
        <strong>Inventory Year:</strong>
        <span>{nationalResult.inventeringsAr || nationalResult.invAr || 'N/A'}</span>
      </div>
      <div class="metric">
        <strong>Number of Areas:</strong>
        <span>{nationalResult.antalAFODelomr || 'N/A'}</span>
      </div>
      <div class="metric">
        <strong>Number of Grids:</strong>
        <span>{nationalResult.antalRutor || 'N/A'}</span>
      </div>
      <div class="metric">
        <strong>Pine Damage (Annual):</strong>
        <span>{nationalResult.arsskadaTallAndel ? (nationalResult.arsskadaTallAndel * 100).toFixed(1) + '%' : 'N/A'}</span>
      </div>
      <div class="metric">
        <strong>Spruce Damage (Annual):</strong>
        <span>{nationalResult.arsskadaGranAndel ? (nationalResult.arsskadaGranAndel * 100).toFixed(1) + '%' : 'N/A'}</span>
      </div>
    </div>
  {/if}

  {#if countyResult}
    <div class="result-section">
      <h3>County: {countyResult.lanNamn || countyResult.omrade || 'Unknown'} (Most Recent)</h3>
      <div class="metric">
        <strong>Inventory Year:</strong>
        <span>{countyResult.invAr || countyResult.inventeringsAr || 'N/A'}</span>
      </div>
      <div class="metric">
        <strong>County Code:</strong>
        <span>{countyResult.lanKod || countyResult.lankod || 'N/A'}</span>
      </div>
      <div class="metric">
        <strong>Region:</strong>
        <span>{countyResult.landsdelNamn || 'N/A'}</span>
      </div>
      {#if countyResult.antalAFODelomr}
        <div class="metric">
          <strong>Number of ÄFO Areas:</strong>
          <span>{countyResult.antalAFODelomr}</span>
        </div>
      {/if}
      {#if countyResult.antalRutor}
        <div class="metric">
          <strong>Number of Grids:</strong>
          <span>{countyResult.antalRutor}</span>
        </div>
      {/if}
      {#if countyResult.arsskadaTallAndel !== undefined}
        <div class="metric">
          <strong>Pine Damage (Annual):</strong>
          <span>{(countyResult.arsskadaTallAndel * 100).toFixed(1)}%</span>
        </div>
      {/if}
      {#if countyResult.arsskadaGranAndel !== undefined}
        <div class="metric">
          <strong>Spruce Damage (Annual):</strong>
          <span>{(countyResult.arsskadaGranAndel * 100).toFixed(1)}%</span>
        </div>
      {/if}
      {#if countyResult.oskadadTallAndel !== undefined}
        <div class="metric">
          <strong>Undamaged Pine:</strong>
          <span>{(countyResult.oskadadTallAndel * 100).toFixed(1)}%</span>
        </div>
      {/if}
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

  .controls {
    display: flex;
    gap: 1rem;
    align-items: flex-end;
    margin-bottom: 1rem;
  }

  label {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    color: #333;
    font-weight: 500;
  }

  select {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
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
    min-width: 180px;
    color: #333;
  }

  .metric span {
    margin-left: 1rem;
    color: #2c5f2d;
    font-weight: 600;
  }
</style>
