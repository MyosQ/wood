<script lang="ts">
  import { onMount } from 'svelte';
  import { get, ApiException } from './lib/api';
  import GrunddataExample from './lib/components/GrunddataExample.svelte';
  import AbinExample from './lib/components/AbinExample.svelte';
  import ThemeToggle from './lib/components/ThemeToggle.svelte';

  let apiStatus = $state('checking...');
  let apiMessage = $state('');
  let errorType = $state('');

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

<div class="min-h-screen bg-background">
  <main class="mx-auto max-w-5xl px-6 py-8">
    <!-- Header with theme toggle -->
    <div class="mb-8 flex items-center justify-between">
      <h1 class="text-4xl font-bold text-primary">
        Skogsstyrelsen API Client
      </h1>
      <ThemeToggle />
    </div>

    <!-- Status Card -->
    <div class="mb-6 rounded-lg border border-border bg-surface p-6 shadow-md">
      <h2 class="mb-4 text-xl font-semibold text-text-primary">
        Backend Status
      </h2>

      <span
        role="status"
        aria-live="polite"
        class="inline-block rounded px-4 py-2 font-semibold border {apiStatus === 'connected'
          ? 'bg-success-bg text-success-text border-success-border'
          : apiStatus === 'error'
          ? 'bg-error-bg text-error-text border-error-border'
          : 'bg-surface text-text-secondary border-border'}"
      >
        {apiStatus}
      </span>

      {#if apiMessage}
        <p class="mt-4 text-text-secondary">{apiMessage}</p>
      {/if}

      {#if errorType && apiStatus === 'error'}
        <p class="mt-2 font-mono text-sm text-text-tertiary">
          Error type: {errorType}
        </p>
      {/if}
    </div>

    <!-- Info Banner -->
    <div class="mb-6 rounded-lg border-l-4 border-primary bg-surface px-6 py-4">
      <p class="text-text-secondary">
        Try the example components below to test the API integration!
      </p>
    </div>

    <!-- Example Components -->
    <div class="space-y-6">
      <GrunddataExample />
      <AbinExample />
    </div>
  </main>
</div>
