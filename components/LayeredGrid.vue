<template>
  <div class="relative w-screen h-screen overflow-hidden">
    <!-- Top layer - Viewport constrained view -->
    <div class="absolute inset-0 overflow-hidden">
      <div
        class="relative w-[2700px] h-[2040px] transform -translate-x-1/2 -translate-y-1/2 left-1/2 top-1/2"
      >
        <div
          v-for="(position, index) in gridPositions"
          :key="`top-${index}`"
          v-if="isFirstLayerItem(index)"
          :style="getItemStyle(position, 0)"
          class="absolute w-40 h-40 bg-blue-500 rounded-lg transition-all duration-300"
        >
          {{ items[index] }}
        </div>
        <!-- Center content - positioned to occupy a grid cell -->
        <div
          :style="getCenterStyle()"
          class="absolute w-80 h-80 bg-white rounded-xl shadow-lg z-50 flex flex-col items-center justify-center"
        >
          <h2 class="text-3xl font-bold mb-4">Center Title</h2>
          <p class="text-lg text-gray-600 px-8 text-center">
            This is the centered content that remains visible while other items
            shift around it.
          </p>
        </div>
      </div>
    </div>

    <!-- Middle layer -->
    <div class="absolute inset-0 -z-10">
      <div
        class="relative w-[2700px] h-[2040px] transform -translate-x-1/2 -translate-y-1/2 left-1/2 top-1/2"
      >
        <div
          v-for="(position, index) in gridPositions"
          :key="`middle-${index}`"
          v-if="isSecondLayerItem(index)"
          :style="getItemStyle(position, 1)"
          class="absolute w-40 h-40 bg-green-500 rounded-lg opacity-80"
        >
          {{ items[index] }}
        </div>
      </div>
    </div>

    <!-- Bottom layer -->
    <div class="absolute inset-0 -z-20">
      <div
        class="relative w-[2700px] h-[2040px] transform -translate-x-1/2 -translate-y-1/2 left-1/2 top-1/2"
      >
        <div
          v-for="(position, index) in gridPositions"
          :key="`bottom-${index}`"
          v-if="isThirdLayerItem(index)"
          :style="getItemStyle(position, 2)"
          class="absolute w-40 h-40 bg-red-500 rounded-lg opacity-60"
        >
          {{ items[index] }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
});

// Grid configuration
const GRID_COLS = Math.ceil(Math.sqrt(props.items.length));
const CELL_SIZE = 160; // Base size of each grid cell

// Calculate the center position
const centerIndices = computed(() => {
  const totalRows = Math.ceil(props.items.length / GRID_COLS);
  const centerRow = Math.floor(totalRows / 2);
  const centerCol = Math.floor(GRID_COLS / 2);
  return {
    row: centerRow,
    col: centerCol,
    index: centerRow * GRID_COLS + centerCol,
  };
});

// Generate grid positions for all items
const gridPositions = computed(() => {
  return props.items.map((_, index) => {
    const row = Math.floor(index / GRID_COLS);
    const col = index % GRID_COLS;

    return {
      baseX: col * CELL_SIZE + (2700 - GRID_COLS * CELL_SIZE) / 2,
      baseY:
        row * CELL_SIZE +
        (2040 - Math.ceil(props.items.length / GRID_COLS) * CELL_SIZE) / 2,
    };
  });
});

// Determine which layer each item belongs to
const itemsPerLayer = Math.ceil(props.items.length / 3);

function isFirstLayerItem(index) {
  return index < itemsPerLayer && index !== centerIndices.value.index;
}

function isSecondLayerItem(index) {
  return (
    index >= itemsPerLayer &&
    index < itemsPerLayer * 2 &&
    index !== centerIndices.value.index
  );
}

function isThirdLayerItem(index) {
  return index >= itemsPerLayer * 2 && index !== centerIndices.value.index;
}

// Get positioned style for each item with random offset
function getItemStyle(position, layerIndex) {
  // Random offset gets smaller for each layer down (creating depth effect)
  const offsetRange = Math.max(20 - layerIndex * 5, 5);
  const randomX = Math.random() * offsetRange * 2 - offsetRange;
  const randomY = Math.random() * offsetRange * 2 - offsetRange;

  return {
    left: `${position.baseX + randomX}px`,
    top: `${position.baseY + randomY}px`,
    transform: `translate(-50%, -50%) scale(${1 - layerIndex * 0.05})`, // Slight scale down for depth
  };
}

// Get style for center content
function getCenterStyle() {
  // Use the center indices to calculate the position
  const centerPosition = {
    baseX:
      centerIndices.value.col * CELL_SIZE + (2700 - GRID_COLS * CELL_SIZE) / 2,
    baseY:
      centerIndices.value.row * CELL_SIZE +
      (2040 - Math.ceil(props.items.length / GRID_COLS) * CELL_SIZE) / 2,
  };

  return {
    left: `${centerPosition.baseX}px`,
    top: `${centerPosition.baseY}px`,
    transform: 'translate(-50%, -50%)',
  };
}
</script>
