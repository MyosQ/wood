<script lang="ts">
  import { getHelalandet, getLan } from '../services/abin';
  import { COUNTIES } from '../examples';
  import { ApiException } from '../api';

  let loading = $state(false);
  let error = $state('');
  let nationalResult: any = $state(null);
  let countyResult: any = $state(null);
  let selectedCounty = $state(COUNTIES.STOCKHOLM);

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

<div class="rounded-lg border border-border bg-surface p-6 shadow-md">
  <h2 class="text-xl font-semibold text-primary">Browsing Inventory Example</h2>
  <p class="mt-2 text-text-secondary">
    View browsing damage statistics from moose and deer inventory (ABIN).
  </p>

  <div class="mt-4 flex flex-wrap items-end gap-4">
    <label class="flex flex-col gap-2">
      <span class="font-medium text-text-primary">County:</span>
      <select
        bind:value={selectedCounty}
        class="rounded-lg border border-border bg-background px-3 py-2 text-text-primary transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
      >
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

    <button
      onclick={fetchBrowsingData}
      disabled={loading}
      class="rounded-lg bg-primary px-6 py-3 font-medium text-white transition-colors hover:bg-primary-dark focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:bg-primary"
    >
      {loading ? 'Loading...' : 'Fetch Browsing Data'}
    </button>
  </div>

  {#if error}
    <div class="mt-4 rounded-lg border border-error-border bg-error-bg p-4 text-error-text">
      {error}
    </div>
  {/if}

  {#if nationalResult}
    <div class="mt-6 rounded-lg bg-background p-4 border border-border">
      <h3 class="mb-3 text-lg font-medium text-text-primary">National Summary (Most Recent)</h3>
      <div class="border-b border-border py-3">
        <span class="inline-block min-w-[180px] font-semibold text-text-primary">Area:</span>
        <span class="ml-4 font-semibold text-primary">{nationalResult.omrade || 'Hela landet'}</span>
      </div>
      <div class="border-b border-border py-3">
        <span class="inline-block min-w-[180px] font-semibold text-text-primary">Inventory Year:</span>
        <span class="ml-4 font-semibold text-primary">{nationalResult.inventeringsAr || nationalResult.invAr || 'N/A'}</span>
      </div>
      <div class="border-b border-border py-3">
        <span class="inline-block min-w-[180px] font-semibold text-text-primary">Number of Areas:</span>
        <span class="ml-4 font-semibold text-primary">{nationalResult.antalAFODelomr || 'N/A'}</span>
      </div>
      <div class="border-b border-border py-3">
        <span class="inline-block min-w-[180px] font-semibold text-text-primary">Number of Grids:</span>
        <span class="ml-4 font-semibold text-primary">{nationalResult.antalRutor || 'N/A'}</span>
      </div>
      <div class="border-b border-border py-3">
        <span class="inline-block min-w-[180px] font-semibold text-text-primary">Pine Damage (Annual):</span>
        <span class="ml-4 font-semibold text-primary">{nationalResult.arsskadaTallAndel ? (nationalResult.arsskadaTallAndel * 100).toFixed(1) + '%' : 'N/A'}</span>
      </div>
      <div class="py-3">
        <span class="inline-block min-w-[180px] font-semibold text-text-primary">Spruce Damage (Annual):</span>
        <span class="ml-4 font-semibold text-primary">{nationalResult.arsskadaGranAndel ? (nationalResult.arsskadaGranAndel * 100).toFixed(1) + '%' : 'N/A'}</span>
      </div>
    </div>
  {/if}

  {#if countyResult}
    <div class="mt-6 rounded-lg bg-background p-4 border border-border">
      <h3 class="mb-3 text-lg font-medium text-text-primary">County: {countyResult.lanNamn || countyResult.omrade || 'Unknown'} (Most Recent)</h3>
      <div class="border-b border-border py-3">
        <span class="inline-block min-w-[180px] font-semibold text-text-primary">Inventory Year:</span>
        <span class="ml-4 font-semibold text-primary">{countyResult.invAr || countyResult.inventeringsAr || 'N/A'}</span>
      </div>
      <div class="border-b border-border py-3">
        <span class="inline-block min-w-[180px] font-semibold text-text-primary">County Code:</span>
        <span class="ml-4 font-semibold text-primary">{countyResult.lanKod || countyResult.lankod || 'N/A'}</span>
      </div>
      <div class="border-b border-border py-3">
        <span class="inline-block min-w-[180px] font-semibold text-text-primary">Region:</span>
        <span class="ml-4 font-semibold text-primary">{countyResult.landsdelNamn || 'N/A'}</span>
      </div>
      {#if countyResult.antalAFODelomr}
        <div class="border-b border-border py-3">
          <span class="inline-block min-w-[180px] font-semibold text-text-primary">Number of ÄFO Areas:</span>
          <span class="ml-4 font-semibold text-primary">{countyResult.antalAFODelomr}</span>
        </div>
      {/if}
      {#if countyResult.antalRutor}
        <div class="border-b border-border py-3">
          <span class="inline-block min-w-[180px] font-semibold text-text-primary">Number of Grids:</span>
          <span class="ml-4 font-semibold text-primary">{countyResult.antalRutor}</span>
        </div>
      {/if}
      {#if countyResult.arsskadaTallAndel !== undefined}
        <div class="border-b border-border py-3">
          <span class="inline-block min-w-[180px] font-semibold text-text-primary">Pine Damage (Annual):</span>
          <span class="ml-4 font-semibold text-primary">{(countyResult.arsskadaTallAndel * 100).toFixed(1)}%</span>
        </div>
      {/if}
      {#if countyResult.arsskadaGranAndel !== undefined}
        <div class="border-b border-border py-3">
          <span class="inline-block min-w-[180px] font-semibold text-text-primary">Spruce Damage (Annual):</span>
          <span class="ml-4 font-semibold text-primary">{(countyResult.arsskadaGranAndel * 100).toFixed(1)}%</span>
        </div>
      {/if}
      {#if countyResult.oskadadTallAndel !== undefined}
        <div class="py-3">
          <span class="inline-block min-w-[180px] font-semibold text-text-primary">Undamaged Pine:</span>
          <span class="ml-4 font-semibold text-primary">{(countyResult.oskadadTallAndel * 100).toFixed(1)}%</span>
        </div>
      {/if}
    </div>
  {/if}
</div>
