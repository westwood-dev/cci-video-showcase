<template>
  <div>
    <!-- <Gallery :items="items" /> -->
    <Grid :items="items" />
  </div>
</template>
<script setup>
const items = Array.from({ length: 27 }, (_, i) => `Item ${i + 1}`);
</script>
