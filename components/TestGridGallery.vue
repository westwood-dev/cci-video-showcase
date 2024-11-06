<template>
  <div class="gallery-container bgColour" id="galleryRoot">
    <!-- Original item -->
    <div
      v-for="i in 3"
      :key="i"
      class="item"
      :style="{
        top: '200px',
        left: `${i * 300}px`,
        backgroundColor: `rgb(${
          i === 1 ? '255,0,0' : i === 2 ? '0,255,0' : '0,0,255'
        })`,
      }"
      @click="handleItemClick($event, i)"
    ></div>

    <!-- Focused item portal -->
    <Teleport to="body" v-if="focusedItem">
      <div
        ref="focusedItemRef"
        class="focused-item"
        :style="focusedItemStyle"
      ></div>
    </Teleport>

    <div v-show="blocker" id="blocker" @click="handleBlockerClick"></div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';

const blocker = ref(false);
const focusedItem = ref(null);
const focusedItemStyle = ref({});
const focusedItemRef = ref(null);

const handleItemClick = async (e, index) => {
  const item = e.currentTarget;
  const rect = item.getBoundingClientRect();

  // First, show the clone at exactly the same position
  focusedItemStyle.value = {
    position: 'fixed',
    top: `${rect.top}px`,
    left: `${rect.left}px`,
    width: `${rect.width}px`,
    height: `${rect.height}px`,
    backgroundColor: item.style.backgroundColor,
  };

  focusedItem.value = { index };
  blocker.value = true;

  // Wait for the clone to be mounted
  await nextTick();

  // Force a reflow
  focusedItemRef.value?.offsetHeight;

  // Add transition class and update position
  focusedItemRef.value?.classList.add('animating');

  focusedItemStyle.value = {
    ...focusedItemStyle.value,
    top: '50%',
    left: '50%',
    width: '80vw',
    height: '80vh',
    transform: 'translate(-50%, -50%)',
  };
};

const handleBlockerClick = () => {
  const originalItem = document.querySelector(
    `.item:nth-child(${focusedItem.value.index})`
  );
  const rect = originalItem.getBoundingClientRect();

  focusedItemStyle.value = {
    ...focusedItemStyle.value,
    top: `${rect.top}px`,
    left: `${rect.left}px`,
    width: '600px',
    height: '350px',
    transform: 'none',
  };

  setTimeout(() => {
    focusedItem.value = null;
    blocker.value = false;
  }, 500);
};
</script>

<style scoped>
.gallery-container {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.item {
  position: absolute;
  width: 600px;
  height: 350px;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.3s ease;
}

.item:hover {
  opacity: 1;
}

.focused-item {
  position: fixed;
  z-index: 1000;
  opacity: 1;
  transition: none;
}

.focused-item.animating {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

#blocker {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 100;
  transition: opacity 0.3s ease;
}
</style>
