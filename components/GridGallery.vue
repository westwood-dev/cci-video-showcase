<template>
  <div class="gallery-container">
    <div
      class="gallery-grid"
      :style="{
        gridTemplateColumns: `repeat(${Math.ceil(
          Math.sqrt(items.length)
        )}, 1fr)`,
      }"
    >
      <div class="gallery-cell" v-for="(item, index) in items" :key="index">
        {{ item }}
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
});
</script>

<style scoped>
.gallery-container {
  width: 100vw;
  height: 100vh;
  /* overflow: hidden; */
  background-color: lightblue;
}

.gallery-grid {
  width: 2700px;
  height: 2040px;
  display: grid;
}
</style>
