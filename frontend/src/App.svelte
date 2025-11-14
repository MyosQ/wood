<script lang="ts">
  import MapInterface from './lib/components/MapInterface.svelte';
  import ThemeToggle from './lib/components/ThemeToggle.svelte';
</script>

<!-- Theme Toggle (fixed position overlay with higher z-index) -->
<div class="fixed top-4 right-4 z-[1000]">
  <ThemeToggle />
</div>

<!-- Map Interface (full viewport) -->
<MapInterface />
