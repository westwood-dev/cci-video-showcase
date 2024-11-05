<template>
  <div
    class="gallery-container bgColour"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <div class="gallery-layer-0" :style="centerLayerStyle">
      <div class="title-cont">
        <h1 class="textColour">Brief one</h1>
        <h1 class="textColour">"light"</h1>
      </div>
    </div>
    <div
      :style="{
        width: containerWidth + 'px',
        height: containerHeight + 'px',
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
      }"
    >
      <div
        v-for="layer in layers"
        :key="layer.index"
        :class="`gallery-layer-${layer.index}`"
        :style="[
          layer.style,
          // { width: containerWidth + 'px', height: containerHeight + 'px' },
        ]"
      >
        <div
          v-for="(item, itemIndex) in layer.items"
          :key="itemIndex"
          class="item"
          @click="handleItemClick(layer.index, itemIndex, item)"
          @mouseenter="handleItemHover(layer.index, itemIndex, item)"
          @mouseleave="handleItemLeave(layer.index, itemIndex, item)"
        >
          <div
            class="item-details"
            :id="'details-' + layer.index + '-' + itemIndex"
          >
            <h1 class="item-details-question textColour">Question</h1>
            <p class="item-details-author textColour">Name(s)</p>
          </div>
        </div>
      </div>
    </div>
    <div
      id="debugText"
      class="textColour"
      style="position: fixed; bottom: 0; right: 0; z-index: 1000"
    >
      X: {{ targetX.toFixed(2) }} Y: {{ targetY.toFixed(2) }}
      <ThemeChanger />
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
// Math.ceil(Math.sqrt(props.items.length))
let containerWidth =
  Math.ceil(Math.sqrt(props.items.length)) * 1000 ||
  100 * props.items.length * 2 ||
  2700;
let containerHeight = containerWidth * 0.75 || 2040;
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

  // map users mouse distance from center to half containerWidth/containerHeight
  targetX.value =
    (event.clientX - centerX) * (containerWidth / containerRect.width);
  targetY.value =
    (event.clientY - centerY) * (containerHeight / containerRect.height);

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
  document.getElementById(
    'details-' + layerIndex + '-' + itemIndex
  ).style.display = 'block';
};

const handleItemLeave = (layerIndex, itemIndex, item) => {
  // console.log(`Left item ${itemIndex} in layer ${layerIndex}`, item);
  document.getElementById(
    'details-' + layerIndex + '-' + itemIndex
  ).style.display = 'none';
};

// Configurable variables
const itemWidth = 600; // Width of each div
const itemHeight = 350; // Height of each div
// const numItems = 8; // Number of divs to generate
// const containerWidth = 600
// const containerHeight = 400
const padding = 20; // Minimum space between items
const centerSize = 200; // Size of center div
const maxDistance = containerWidth / 2; // Maximum distance from center

const positions = ref([]);

// Generate a random position within a circular area around the center
const generatePositionAroundCenter = () => {
  const centerX = containerWidth / 2;
  const centerY = containerHeight / 2;

  // Generate random angle and distance
  const angle = Math.random() * 2 * Math.PI;
  const distance = Math.random() * maxDistance + (centerSize / 2 + padding);

  // Convert polar coordinates to cartesian
  const x = centerX + Math.cos(angle) * distance;
  const y = centerY + Math.sin(angle) * distance;

  return {
    x: Math.max(itemWidth / 2, Math.min(containerWidth - itemWidth / 2, x)),
    y: Math.max(itemHeight / 2, Math.min(containerHeight - itemHeight / 2, y)),
  };
};

// Check if a new position overlaps with existing positions or center div
const hasOverlap = (newPos, existingPositions) => {
  // Check overlap with center div
  const centerX = containerWidth / 2;
  const centerY = containerHeight / 2;
  const centerOverlap =
    Math.abs(newPos.x - centerX) < (itemWidth + centerSize) / 2 + padding &&
    Math.abs(newPos.y - centerY) < (itemHeight + centerSize) / 2 + padding;

  if (centerOverlap) return true;

  // Check overlap with other items
  return existingPositions.some((pos) => {
    const xOverlap = Math.abs(newPos.x - pos.x) < itemWidth + padding;
    const yOverlap = Math.abs(newPos.y - pos.y) < itemHeight + padding;
    return xOverlap && yOverlap;
  });
};

const generatePositions = (numItems) => {
  const newPositions = [];

  console.log('Generating ' + numItems + ' positions.');

  for (let i = 0; i < numItems; i++) {
    let attempts = 0;
    let validPosition = false;
    let position;

    while (!validPosition && attempts < 100) {
      const pos = generatePositionAroundCenter();

      position = {
        x: pos.x,
        y: pos.y,
        id: i,
      };

      if (!hasOverlap(position, newPositions)) {
        validPosition = true;
        newPositions.push(position);
      }

      attempts++;
    }

    if (!validPosition) {
      console.warn(`Could not find valid position for item ${i}`);
    }
  }

  positions.value = newPositions;
};

onMounted(() => {
  // Initialize inactivity timer
  startInactivityTimer();

  generatePositions(props.items.length);
  console.log(positions.value);

  let counter = 0;

  layers.value.forEach((layer) => {
    layer.items.forEach((_, itemIndex) => {
      // let top, left;
      // const padding = 100; // Padding to leave a black space in the center

      // do {
      //   top = Math.random() * containerHeight;
      //   left = Math.random() * containerWidth;
      // } while (
      //   top > padding &&
      //   top < containerHeight - padding &&
      //   left > padding &&
      //   left < containerWidth - padding
      // );

      if (counter >= positions.value.length) {
        console.warn('Not enough positions for all items');
        return;
      }
      const { x, y } = positions.value[counter];
      const left = x || 0;
      const top = y || 0;
      counter++;

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

.title-cont {
  min-width: 250px;
  width: 600px;
  height: 200px;
  /* background-color: blueviolet; */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
}

.title-cont h1 {
  font-size: 8rem;
  font-family: 'Bigger Display', sans-serif;
  text-transform: uppercase;
  margin: 0;
  margin-bottom: -3rem;
}

.title-cont h1:first-child {
  margin-left: -10rem;
}

.title-cont h1:last-child {
  margin-right: -10rem;
}

.gallery-layer-0 {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  will-change: transform;
  pointer-events: none;
}

.gallery-layer-1,
.gallery-layer-2,
.gallery-layer-3 {
  position: absolute;
  /* top: -50%; */
  /* left: -50%; */
  will-change: transform;
  pointer-events: none;
}

.item {
  position: absolute;
  width: 600px;
  /* aspect-ratio: 16/9; */
  height: 350px;
  background-color: rgba(255, 0, 0, 0.5);
  pointer-events: auto;
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.item-details {
  display: none;
  position: absolute;
  bottom: 0;
  max-width: 80%;
  padding: 1rem;
}

.item-details-question {
  font-size: 2rem;
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
