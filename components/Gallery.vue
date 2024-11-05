<template>
  <div
    class="gallery-container"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <div class="gallery-layer-0" :style="centerLayerStyle">
      <div class="title-cont">Center Content</div>
    </div>
    <div
      v-for="layer in layers"
      :key="layer.index"
      :class="`gallery-layer-${layer.index}`"
      :style="layer.style"
    >
      <div
        v-for="(item, itemIndex) in layer.items"
        :key="itemIndex"
        class="item"
        @click="handleItemClick(layer.index, itemIndex, item)"
        @mouseenter="handleItemHover(layer.index, itemIndex, item)"
        @mouseleave="handleItemLeave(layer.index, itemIndex, item)"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
});

const containerWidth = 2700;
const containerHeight = 2040;
const INACTIVITY_TIMEOUT = 30000; // 30 seconds in milliseconds

const centerLayerStyle = reactive({ transform: 'translate3d(0px, 0px, 0px)' });
let inactivityTimer = null;
let isResetting = ref(false);

const layers = ref([
  {
    index: 1,
    style: reactive({
      transform: 'translate3d(0px, 0px, 0px)',
      zIndex: 3,
    }),
    items: [],
  },
  {
    index: 2,
    style: reactive({
      transform: 'translate3d(0px, 0px, 0px)',
      zIndex: 2,
    }),
    items: [],
  },
  {
    index: 3,
    style: reactive({
      transform: 'translate3d(0px, 0px, 0px)',
      zIndex: 1,
    }),
    items: [],
  },
]);

for (const [index, item] of props.items.entries()) {
  const layerIndex = Math.floor(index / (props.items.length / 3));
  layers.value[layerIndex].items.push(item);
}

const mouseX = ref(0);
const mouseY = ref(0);
const targetX = ref(0);
const targetY = ref(0);

let animationFrameId;

const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);

// Reset function
const resetPosition = () => {
  isResetting.value = true;
  targetX.value = 0;
  targetY.value = 0;
};

// Start inactivity timer
const startInactivityTimer = (multiplier = 1) => {
  clearTimeout(inactivityTimer);
  inactivityTimer = setTimeout(() => {
    resetPosition();
  }, INACTIVITY_TIMEOUT * multiplier);
};

const handleMouseMove = (event) => {
  isResetting.value = false;
  const containerRect = document
    .querySelector('.gallery-container')
    .getBoundingClientRect();
  const centerX = containerRect.left + containerRect.width / 2;
  const centerY = containerRect.top + containerRect.height / 2;

  targetX.value = (event.clientX - centerX) * 2;
  targetY.value = (event.clientY - centerY) * 2;

  // Reset inactivity timer on mouse move
  startInactivityTimer();
};

const handleMouseLeave = () => {
  // resetPosition();
  startInactivityTimer(0.3);
};

const handleItemClick = (layerIndex, itemIndex, item) => {
  // console.log(`Clicked item ${itemIndex} in layer ${layerIndex}`, item);
};

const handleItemHover = (layerIndex, itemIndex, item) => {
  // console.log(`Hovering item ${itemIndex} in layer ${layerIndex}`, item);
};

const handleItemLeave = (layerIndex, itemIndex, item) => {
  // console.log(`Left item ${itemIndex} in layer ${layerIndex}`, item);
};

onMounted(() => {
  // Initialize inactivity timer
  startInactivityTimer();

  layers.value.forEach((layer) => {
    layer.items.forEach((_, itemIndex) => {
      let top, left;
      const padding = 200; // Padding to leave a black space in the center

      do {
        top = Math.random() * containerHeight;
        left = Math.random() * containerWidth;
      } while (
        top > padding &&
        top < containerHeight - padding &&
        left > padding &&
        left < containerWidth - padding
      );

      const item = document.querySelectorAll(
        `.gallery-layer-${layer.index} .item`
      )[itemIndex];
      if (item) {
        item.style.top = `${top}px`;
        item.style.left = `${left}px`;
      }
    });
  });

  function animate() {
    // Animate center layer
    const centerCurrentX = parseFloat(
      centerLayerStyle.transform.split('(')[1].split(',')[0]
    );
    const centerCurrentY = parseFloat(
      centerLayerStyle.transform.split(', ')[1].split(',')[0]
    );

    const easingMultiplier = isResetting.value ? 0.5 : 0.05; // Faster easing when resetting

    const centerNewX =
      centerCurrentX +
      (targetX.value * 0.02 + centerCurrentX) * -easingMultiplier;
    const centerNewY =
      centerCurrentY +
      (targetY.value * 0.02 + centerCurrentY) * -easingMultiplier;

    centerLayerStyle.transform = `translate3d(${centerNewX}px, ${centerNewY}px, 0px)`;

    // Animate other layers
    layers.value.forEach((layer) => {
      const layerOffsetMultiplier = 1 + layer.index * 0.15;

      const currentX = parseFloat(
        layer.style.transform.split('(')[1].split(',')[0]
      );
      const currentY = parseFloat(
        layer.style.transform.split(', ')[1].split(',')[0]
      );

      const easingFactor = isResetting.value ? 0.03 : 0.03; // Faster easing when resetting
      const deltaX =
        (targetX.value + currentX) * -easingFactor * layerOffsetMultiplier;
      const deltaY =
        (targetY.value + currentY) * -easingFactor * layerOffsetMultiplier;

      const newX = currentX + easeOutCubic(Math.abs(deltaX) / 100) * deltaX;
      const newY = currentY + easeOutCubic(Math.abs(deltaY) / 100) * deltaY;

      layer.style.transform = `translate3d(${newX}px, ${newY}px, 0px)`;
    });

    animationFrameId = requestAnimationFrame(animate);
  }

  animate();
});

onUnmounted(() => {
  cancelAnimationFrame(animationFrameId);
  clearTimeout(inactivityTimer);
});
</script>

<style scoped>
.gallery-container {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.gallery-layer-0 {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 4;
  will-change: transform;
  pointer-events: none;
}

.gallery-layer-1,
.gallery-layer-2,
.gallery-layer-3 {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 2700px;
  height: 2040px;
  will-change: transform;
  pointer-events: none;
}

.item {
  position: absolute;
  width: 600px;
  aspect-ratio: 16/9;
  /* height: 100px; */
  background-color: rgba(255, 0, 0, 0.5);
  pointer-events: auto;
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
  transform: translate(-50%, -50%);
}

.item:hover {
  background-color: rgba(255, 0, 0, 0.8);
  transform: scale(1.1) translate(-50%, -50%);
}

.gallery-layer-1 .item {
  background-color: rgba(255, 0, 0, 0.5);
}

.gallery-layer-2 .item {
  background-color: rgba(0, 255, 0, 0.5);
}

.gallery-layer-3 .item {
  background-color: rgba(0, 0, 255, 0.5);
}
</style>
