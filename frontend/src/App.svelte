<script lang="ts">
  import { onMount } from 'svelte';
  import { get, ApiException } from './lib/api';
  import GrunddataExample from './lib/components/GrunddataExample.svelte';
  import AbinExample from './lib/components/AbinExample.svelte';

  let apiStatus = 'checking...';
  let apiMessage = '';
  let errorType = '';

  onMount(async () => {
    try {
      const response = await get<{ message: string; version: string }>('/');
      apiMessage = `${response.message} (v${response.version})`;
      apiStatus = 'connected';
    } catch (error) {
      apiStatus = 'error';
      if (error instanceof ApiException) {
        apiMessage = error.message;
        errorType = error.errorType || 'unknown';
      } else {
        apiMessage = error instanceof Error ? error.message : 'Unknown error';
        errorType = 'unknown';
      }
    }
  });
</script>

<main>
  <h1>Skogsstyrelsen API Client</h1>

  <div class="status-card">
    <h2>Backend Status</h2>
    <p class="status" class:connected={apiStatus === 'connected'} class:error={apiStatus === 'error'}>
      {apiStatus}
    </p>
    {#if apiMessage}
      <p class="message">{apiMessage}</p>
    {/if}
    {#if errorType && apiStatus === 'error'}
      <p class="error-type">Error type: {errorType}</p>
    {/if}
  </div>

  <div class="info">
    <p>Try the example components below to test the API integration!</p>
  </div>

  <GrunddataExample />
  <AbinExample />
</main>

<style>
  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    font-family: system-ui, -apple-system, sans-serif;
  }

  h1 {
    color: #2c5f2d;
    margin-bottom: 2rem;
  }

  .status-card {
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .status-card h2 {
    margin-top: 0;
    font-size: 1.2rem;
    color: #333;
  }

  .status {
    font-weight: bold;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    display: inline-block;
  }

  .status.connected {
    background-color: #d4edda;
    color: #155724;
  }

  .status.error {
    background-color: #f8d7da;
    color: #721c24;
  }

  .message {
    margin-top: 1rem;
    color: #666;
  }

  .info {
    background-color: #f8f9fa;
    border-left: 4px solid #2c5f2d;
    padding: 1rem 1.5rem;
    border-radius: 4px;
  }

  .info p {
    margin: 0;
    color: #555;
  }

  .error-type {
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: #999;
    font-family: monospace;
  }
</style>
