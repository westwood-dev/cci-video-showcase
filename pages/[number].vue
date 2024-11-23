<template>
  <div style="overflow: hidden">
    <Grid v-if="route.query.view == 'grid' && data" :data="data || []" />
    <Gallery v-else v-if="data" :data="data" />
    <!-- <TestGridGallery /> -->
  </div>
</template>
<script setup lang="ts">
import type { IBrief } from '@/types/brief.type';

const route = useRoute();

const items = ref([]);

const numberTextLookup = {
  1: 'one',
  2: 'two',
  3: 'three',
  4: 'four',
};

const { params } = useRoute();

let number = params.number;

if (typeof number === 'string' && !isNaN(Number(number))) {
  // Convert string to number if it's a numeric string
  number = Number(number);
}

if (typeof number === 'number') {
  number = numberTextLookup[number];
}

const { data } = await useFetch<IBrief>(`/results_${number}.json`);

onMounted(() => {
  console.log(params.number, number);
  console.log(data.value);
  // items.value = data.value;
});
</script>

<style scoped>
html {
  overflow: hidden;
}
</style>
