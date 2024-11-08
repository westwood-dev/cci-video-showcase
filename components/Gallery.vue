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
        :style="[layer.style]"
      >
        <div
          v-for="(item, itemIndex) in layer.items"
          :key="itemIndex"
          class="item"
          :id="`item-${layer.index}-${itemIndex}`"
          :style="{ backgroundImage: `url(${item.thumbURL})` }"
          @click="handleItemClick($event, layer.index, itemIndex, item)"
          @mouseenter="handleItemHover(layer.index, itemIndex, item)"
          @mouseleave="handleItemLeave(layer.index, itemIndex, item)"
        >
          <div
            class="item-details"
            :id="'details-' + layer.index + '-' + itemIndex"
          >
            <h1 class="item-details-question textColour">
              {{
                item.title.length > 80
                  ? item.title.slice(0, 80).split(' ').slice(0, -1).join(' ') +
                    '...'
                  : item.title
              }}
            </h1>
            <p class="item-details-author textColour">
              {{ item['authors-array'].join(', ') }}
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
        <div class="close-btn textColour" @click="handleBlockerClick">
          <Icon name="material-symbols:close" size="2rem" />
        </div>
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
          <h3>{{ focusedItem.itemData['authors-array'].join(', ') }}</h3>
          <template v-if="focusedItem.itemData['final-proposition'].length > 0">
            <h2>Final Proposition</h2>
            <p>{{ focusedItem.itemData['final-proposition'] }}</p>
          </template>
          <template v-if="focusedItem.itemData['insights'].length > 0">
            <h2>Insights</h2>
            <p>{{ focusedItem.itemData['insights'] }}</p>
          </template>
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

let containerWidth =
  Math.ceil(Math.sqrt(props.items.length)) * 1000 ||
  100 * props.items.length * 2 ||
  2700;
let containerHeight = containerWidth * 0.75 || 2040;
const INACTIVITY_TIMEOUT = 30000;

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

const resetPosition = () => {
  isResetting.value = true;
  currentOffset.value = { x: 0, y: 0 };
  targetX.value = 0;
  targetY.value = 0;
};

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

  targetX.value =
    (event.clientX - centerX) * (containerWidth / containerRect.width);
  targetY.value =
    (event.clientY - centerY) * (containerHeight / containerRect.height);

  startInactivityTimer();
};

const handleMouseLeave = () => {
  startInactivityTimer(0.3);
};

const focusedItem = ref(null);
const focusedItemStyle = ref({});

const handleItemClick = async (e, layerIndex, itemIndex, itemData) => {
  const item = e.target;
  const itemRect = item.getBoundingClientRect();

  blocker.value = true;

  focusedItem.value = {
    id: `item-${layerIndex}-${itemIndex}`,
    layerIndex,
    itemIndex,
    initialRect: itemRect,
    animating: true,
    itemData,
  };

  focusedItemStyle.value = {
    position: 'fixed',
    top: `${itemRect.top}px`,
    left: `${itemRect.left}px`,
    width: `${itemRect.width}px`,
    height: `${itemRect.height}px`,
    transform: 'none',
    transition: 'none',
  };

  void document.body.offsetHeight;

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

  const itemRect = originalItem.getBoundingClientRect();

  focusedItem.value.animating = true;

  focusedItemStyle.value = {
    ...focusedItemStyle.value,
    top: `${itemRect.top}px`,
    left: `${itemRect.left}px`,
    width: `${itemRect.width}px`,
    height: `${itemRect.height}px`,
    transform: 'none',
    transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)',
  };

  await new Promise((resolve) => setTimeout(resolve, 500));

  focusedItem.value = null;
  blocker.value = false;
};

const handleFocusedItemClick = (e) => {
  e.stopPropagation();
};

const handleItemHover = (layerIndex, itemIndex, item) => {
  document.getElementById(
    'details-' + layerIndex + '-' + itemIndex
  ).style.display = 'flex';
  document.getElementById(
    'details-' + layerIndex + '-' + itemIndex
  ).style.opacity = 1;
};

const handleItemLeave = (layerIndex, itemIndex, item) => {
  document.getElementById(
    'details-' + layerIndex + '-' + itemIndex
  ).style.opacity = 0;
  setTimeout(() => {
    document.getElementById(
      'details-' + layerIndex + '-' + itemIndex
    ).style.display = 'none';
  }, 300);
};

let itemWidth = 600;
let itemHeight = 350;
const padding = 20;
const centerSize = 500;
const maxDistance = containerWidth / 2;

const positions = ref([]);

const generatePositionAroundCenter = () => {
  const centerX = containerWidth / 2;
  const centerY = containerHeight / 2;

  const angle = Math.random() * 2 * Math.PI;
  const distance = Math.random() * maxDistance + (centerSize / 2 + padding);

  const x = centerX + Math.cos(angle) * distance;
  const y = centerY + Math.sin(angle) * distance;

  return {
    x: Math.max(itemWidth / 2, Math.min(containerWidth - itemWidth / 2, x)),
    y: Math.max(itemHeight / 2, Math.min(containerHeight - itemHeight / 2, y)),
  };
};

const hasOverlap = (newPos, existingPositions) => {
  const centerX = containerWidth / 2;
  const centerY = containerHeight / 2;
  const centerOverlap =
    Math.abs(newPos.x - centerX) < (itemWidth + centerSize) / 2 + padding &&
    Math.abs(newPos.y - centerY) < (itemHeight + centerSize) / 2 + padding;

  if (centerOverlap) return true;

  return existingPositions.some((pos) => {
    const xOverlap = Math.abs(newPos.x - pos.x) < itemWidth + padding;
    const yOverlap = Math.abs(newPos.y - pos.y) < itemHeight + padding;
    return xOverlap && yOverlap;
  });
};

const generatePositions = (numItems) => {
  const newPositions = [];

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
  startInactivityTimer();

  itemWidth = window.innerWidth < 768 ? 300 : 600;
  itemHeight = window.innerWidth < 768 ? 125 : 350;

  generatePositions(props.items.length);

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
    const centerCurrentX = parseFloat(
      centerLayerStyle.transform.split('(')[1].split(',')[0]
    );
    const centerCurrentY = parseFloat(
      centerLayerStyle.transform.split(', ')[1].split(',')[0]
    );

    const easingMultiplier = isResetting.value ? 0.5 : 0.05;

    const centerNewX =
      centerCurrentX +
      (targetX.value * 0.02 + centerCurrentX) * -easingMultiplier;
    const centerNewY =
      centerCurrentY +
      (targetY.value * 0.02 + centerCurrentY) * -easingMultiplier;

    centerLayerStyle.transform = `translate3d(${centerNewX}px, ${centerNewY}px, 0px)`;

    layers.value.forEach((layer) => {
      const layerOffsetMultiplier = 1 + layer.index * 0.15;

      const currentX = parseFloat(
        layer.style.transform.split('(')[1].split(',')[0]
      );
      const currentY = parseFloat(
        layer.style.transform.split(', ')[1].split(',')[0]
      );

      const easingFactor = isResetting.value ? 0.03 : 0.03;
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

const lastTouchPos = ref({ x: 0, y: 0 });
const currentOffset = ref({ x: 0, y: 0 });
const isDragging = ref(false);
const interactionType = ref('none');

const handleTouchStart = (e) => {
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

  isResetting.value = false;

  const touchX = e.touches[0].clientX;
  const touchY = e.touches[0].clientY;

  const deltaX = touchX - lastTouchPos.value.x;
  const deltaY = touchY - lastTouchPos.value.y;

  currentOffset.value = {
    x: currentOffset.value.x + deltaX,
    y: currentOffset.value.y + deltaY,
  };

  targetX.value = currentOffset.value.x;
  targetY.value = currentOffset.value.y;

  layers.value.forEach((layer) => {
    const layerOffsetMultiplier = 1 + layer.index * 0.15;
    const newX = currentOffset.value.x * layerOffsetMultiplier;
    const newY = currentOffset.value.y * layerOffsetMultiplier;

    layer.style.transform = `translate3d(${newX}px, ${newY}px, 0px)`;
  });

  const centerMultiplier = 0.02;
  centerLayerStyle.transform = `translate3d(${
    currentOffset.value.x * centerMultiplier
  }px, ${currentOffset.value.y * centerMultiplier}px, 0px)`;

  lastTouchPos.value = {
    x: touchX,
    y: touchY,
  };
};

const handleTouchEnd = () => {
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
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
  position: absolute;
  left: 0;
  top: -2rem;
  padding: 1rem 0;
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
  flex-direction: column;
  justify-content: flex-end;
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 100%;
  padding: 1rem;
  padding-right: 15%;
  background-color: rgba(var(--bg), 0.8);
  opacity: 0;
  transition: opacity 0.3s ease-out;
}

.item-details-question {
  font-size: 3rem;
  font-family: 'Bigger Display', sans-serif;
  text-transform: uppercase;
  line-height: 3rem;
}

.item {
  position: absolute;
  width: 600px;
  height: 350px;
  pointer-events: auto;
  cursor: pointer;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px rgb(0, 0, 0);
  opacity: 0.5;
  transition: transform 0.3s ease, opacity 0.3s ease;
  background-position: center;
  background-size: cover;
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
  padding-top: 4rem;
}

.focused-item-container .close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  cursor: pointer;
}

.focused-item-container.animating {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.item-clone {
  width: 100%;
  position: relative;
  /* background-color: blueviolet !important; */
}

.item-clone video {
  width: calc(100% - 2rem);
  margin: 0 1rem;
  max-height: 70vh;
  height: auto;
  object-fit: contain;
}

.focused-item-details {
  max-width: 100%;
  padding: 1rem;
}

.focused-item-details h1 {
  font-size: 3rem;
  line-height: 3rem;
  text-transform: uppercase;
  font-family: 'Bigger Display', sans-serif;
}
.focused-item-details h2 {
  font-size: 2rem;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  font-weight: 800;
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

@media screen and (max-width: 768px) {
  .gallery-container {
    touch-action: none;
  }
  .title-cont {
    max-width: 360px;
    min-height: 150px;
    height: 40vw;
  }
  .title-cont h1 {
    font-size: 20vw;
  }
  .title-cont .controls {
    height: 6vh;
    flex-direction: row-reverse;
  }

  .title-cont .controls .control {
    font-size: 1rem;
  }

  .title-cont .controls .control:nth-child(1) {
    display: none;
  }

  .item {
    width: 300px;
    height: 175px;
  }

  .focused-item-details h1 {
    font-size: 2rem;
    margin-bottom: 0;
    line-height: 2rem;
  }

  .focused-item-details h3 {
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }
}
</style>
