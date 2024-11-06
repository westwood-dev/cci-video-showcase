<template>
  <div
    class="gallery-container bgColour"
    id="galleryRoot"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <div class="gallery-layer-0" :style="centerLayerStyle">
      <div class="title-cont">
        <h1 class="textColour">Brief one</h1>
        <h1 class="textColour">"light"</h1>
        <div class="controls">
          <button class="control textColour" @click="resetPosition">
            Reset
          </button>
          <ThemeChanger class="control" />
          <button class="control textColour" @click="changeToGridView">
            Grid View
          </button>
        </div>
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
        pointerEvents: 'none',
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
          :id="`item-${layer.index}-${itemIndex}`"
          :style="{ backgroundImage: `url(${item.imageURL})` }"
          @click="handleItemClick($event, layer.index, itemIndex, item)"
          @mouseenter="handleItemHover(layer.index, itemIndex, item)"
          @mouseleave="handleItemLeave(layer.index, itemIndex, item)"
        >
          <div
            class="item-details"
            :id="'details-' + layer.index + '-' + itemIndex"
          >
            <h1 class="item-details-question textColour">{{ item.title }}</h1>
            <p class="item-details-author textColour">
              {{ item.authors.join(', ') }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Focused item portal -->
    <Teleport to="body" v-if="focusedItem">
      <div
        :class="[
          'bgColour',
          'focused-item-container',
          focusedItem.animating ? 'animating' : '',
        ]"
        :style="focusedItemStyle"
        @click="handleFocusedItemClick"
      >
        <div class="close-btn">close</div>
        <div class="item-clone">
          <video
            :src="focusedItem.itemData.videoURL || '@/assets/video/000.mp4'"
            muted
            autoplay
            controls
            loop
          ></video>
        </div>
        <div class="focused-item-details bgColour textColour">
          <h1>{{ focusedItem.itemData.title }}</h1>
          <h3>{{ focusedItem.itemData.authors.join(', ') }}</h3>
          <p class="textColour">{{ focusedItem.itemData.description }}</p>
          <!-- {{ focusedItem }} -->
        </div>
      </div>
    </Teleport>

    <!-- <Transition name="fade"> -->
    <div
      id="blocker"
      @click="handleBlockerClick"
      :style="{
        opacity: blocker ? 1 : 0,
        pointerEvents: blocker ? 'auto' : 'none',
      }"
    ></div>
    <!-- </Transition> -->

    <DevOnly>
      <div
        id="debugText"
        class="textColour"
        style="position: fixed; bottom: 0; right: 0; z-index: 1000"
      >
        isResetting: {{ isResetting }} X: {{ targetX.toFixed(2) }} Y:
        {{ targetY.toFixed(2) }}<br />
        Blocker:
        {{ blocker }}
        <ThemeChanger />
        <button @click="changeToGridView">Grid View</button>
      </div>
    </DevOnly>
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

const router = useRouter();

const changeToGridView = () => {
  console.log('Changing to grid view');
  router.push({ query: { view: 'grid' } });
};

const targetX = ref(0);
const targetY = ref(0);

const blocker = ref(false);

let animationFrameId;

const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);

// Reset function
const resetPosition = () => {
  isResetting.value = true;
  currentOffset.value = { x: 0, y: 0 };
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
  if (blocker.value) {
    return;
  }

  interactionType.value = 'mouse';
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

const focusedItem = ref(null);
const focusedItemStyle = ref({});

const handleItemClick = async (e, layerIndex, itemIndex, itemData) => {
  const item = e.target;
  const itemRect = item.getBoundingClientRect();

  // First set the blocker to be visible but fully transparent
  blocker.value = true;

  // Create initial position data
  focusedItem.value = {
    id: `item-${layerIndex}-${itemIndex}`,
    layerIndex,
    itemIndex,
    initialRect: itemRect,
    animating: true,
    itemData,
  };

  // Set initial position and size exactly matching the clicked item
  focusedItemStyle.value = {
    position: 'fixed',
    top: `${itemRect.top}px`,
    left: `${itemRect.left}px`,
    width: `${itemRect.width}px`,
    height: `${itemRect.height}px`,
    transform: 'none',
    transition: 'none', // Ensure no transition for initial positioning
  };

  // Force a reflow to ensure the initial position is rendered
  void document.body.offsetHeight;

  // Now add the transition and animate to the center
  requestAnimationFrame(() => {
    focusedItemStyle.value = {
      ...focusedItemStyle.value,
      top: '50%',
      left: '50%',
      width: window.innerWidth < 768 ? '90vw' : '60vw',
      height: '80vh',
      transform: 'translate(-50%, -50%)',
      transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)',
    };
  });

  // Remove animating class after animation completes
  setTimeout(() => {
    if (focusedItem.value) {
      focusedItem.value.animating = false;
    }
  }, 500);
};

const handleBlockerClick = async () => {
  if (!focusedItem.value) return;

  const originalItem = document.getElementById(focusedItem.value.id);
  if (!originalItem) {
    blocker.value = false;
    focusedItem.value = null;
    return;
  }

  // Get the current position of the original item
  const itemRect = originalItem.getBoundingClientRect();

  // Set animating flag
  focusedItem.value.animating = true;

  // Update transition and animate back to original position
  focusedItemStyle.value = {
    ...focusedItemStyle.value,
    top: `${itemRect.top}px`,
    left: `${itemRect.left}px`,
    width: `${itemRect.width}px`,
    height: `${itemRect.height}px`,
    transform: 'none',
    transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)',
  };

  // Wait for animation to complete before removing
  await new Promise((resolve) => setTimeout(resolve, 500));

  focusedItem.value = null;
  blocker.value = false;
};

const handleFocusedItemClick = (e) => {
  e.stopPropagation();
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
// const itemWidth = window.innerWidth < 768 ? 300 : 600; // Width of each div
// const itemHeight = window.innerWidth < 768 ? 125 : 350; // Height of each div
let itemWidth = 600; // Width of each div
let itemHeight = 350; // Height of each div
const padding = 20; // Minimum space between items
const centerSize = 500; // Size of center div
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

  itemWidth = window.innerWidth < 768 ? 300 : 600; // Width of each div
  itemHeight = window.innerWidth < 768 ? 125 : 350; // Height of each div

  generatePositions(props.items.length);
  console.log(positions.value);

  let counter = 0;

  layers.value.forEach((layer) => {
    layer.items.forEach((_, itemIndex) => {
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

// Mobile touch events

const lastTouchPos = ref({ x: 0, y: 0 });
const currentOffset = ref({ x: 0, y: 0 });
const isDragging = ref(false);
const interactionType = ref('none');

// Replace existing touch handlers with these:
const handleTouchStart = (e) => {
  // console.log('Touch start');
  interactionType.value = 'touch';
  cancelAnimationFrame(animationFrameId);
  isDragging.value = true;
  lastTouchPos.value = {
    x: e.touches[0].clientX,
    y: e.touches[0].clientY,
  };
};

const handleTouchMove = (e) => {
  if (!isDragging.value) return;
  e.preventDefault();

  // console.log('Touch move');
  isResetting.value = false;

  const touchX = e.touches[0].clientX;
  const touchY = e.touches[0].clientY;

  // Calculate the distance moved
  const deltaX = touchX - lastTouchPos.value.x;
  const deltaY = touchY - lastTouchPos.value.y;

  // Update the offset
  currentOffset.value = {
    x: currentOffset.value.x + deltaX,
    y: currentOffset.value.y + deltaY,
  };

  // Update target values for inactivity reset
  targetX.value = currentOffset.value.x;
  targetY.value = currentOffset.value.y;

  // Update layers directly based on current offset
  layers.value.forEach((layer) => {
    const layerOffsetMultiplier = 1 + layer.index * 0.15;
    const newX = currentOffset.value.x * layerOffsetMultiplier;
    const newY = currentOffset.value.y * layerOffsetMultiplier;

    layer.style.transform = `translate3d(${newX}px, ${newY}px, 0px)`;
  });

  // Update center layer
  const centerMultiplier = 0.02;
  centerLayerStyle.transform = `translate3d(${
    currentOffset.value.x * centerMultiplier
  }px, ${currentOffset.value.y * centerMultiplier}px, 0px)`;

  // Save current position for next move
  lastTouchPos.value = {
    x: touchX,
    y: touchY,
  };
};

const handleTouchEnd = () => {
  // console.log('Touch end');
  isDragging.value = false;
};
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
  width: 35rem;
  height: 16rem;
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

.title-cont h1:nth-child(1) {
  /* margin-left: -10vw; */
  position: absolute;
  top: 0;
  left: 0;
}

.title-cont h1:nth-child(2) {
  /* margin-right: -10vw; */
  position: absolute;
  bottom: 0;
  right: 0;
}

.title-cont .controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  position: absolute;
  left: 0;
  bottom: 0;
  padding: 1rem;
  height: 6rem;
  pointer-events: none;
}

.title-cont .controls .control {
  pointer-events: all;
}

.gallery-layer-0 {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  will-change: transform;
  pointer-events: none;
  z-index: 4;
}

.gallery-layer-1,
.gallery-layer-2,
.gallery-layer-3 {
  position: absolute;
  will-change: transform;
  pointer-events: none;
}

.item-details {
  display: none;
  position: absolute;
  bottom: 0;
  max-width: 80%;
  padding: 1rem;
}

.item-details-question {
  font-size: 3rem;
  font-family: 'Bigger Display', sans-serif;
  text-transform: uppercase;
  margin-bottom: -1rem;
}

.item {
  position: absolute;
  width: 600px;
  height: 350px;
  background-color: rgba(255, 0, 0, 0.5);
  pointer-events: auto;
  cursor: pointer;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px rgb(0, 0, 0);
  opacity: 0.5;
  transition: transform 0.3s ease, opacity 0.3s ease;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.item:hover {
  transform: scale(1.1) translate(-50%, -50%);
  opacity: 1;
}

.focused-item-container {
  position: fixed;
  z-index: 1000;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  overflow-y: scroll;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 1rem;
}

.focused-item-container.animating {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.item-clone {
  max-width: 100%;
  position: relative;
  background-color: blueviolet;
}

.item-clone video {
  width: 100%;
  height: auto;
  object-fit: contain;
}

.focused-item-details {
  max-width: 100%;
  padding: 1rem;
}

.focused-item-details h1 {
  font-size: 3rem;
  text-transform: uppercase;
  font-family: 'Bigger Display', sans-serif;
  margin-bottom: -1rem;
}

.focused-item-details h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

#blocker {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 100;
  /* opacity: 0; */
  transition: opacity 0.5s ease;
}

/* #blocker[style*='display: block'] {
  opacity: 1;
} */

@media screen and (max-width: 768px) {
  .gallery-container {
    touch-action: none;
  }
  .title-cont {
    max-width: 90vw;
    height: 20vh;
  }
  .title-cont h1 {
    font-size: 10vh;
  }
  .title-cont .controls {
    height: 6vh;
    flex-direction: column;
  }

  .title-cont .controls .control {
    font-size: 1rem;
  }

  .title-cont .controls .control:nth-child(1) {
    display: none;
  }

  .item {
    width: 300px;
    height: 125px;
  }

  .focused-item-container {
    /* width: 95vw !important;
    height: 95vh !important; */
  }
}
</style>
