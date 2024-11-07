<template>
  <div class="grid-comp-cont bgColour" @scroll="handleScroll">
    <div class="title-cont textColour" :style="{ opacity: titleOpacity }">
      <h1>brief one</h1>
      <h1>"light"</h1>
      <div class="controls">
        <ThemeChanger class="control" />
        <button class="control textColour" @click="changeToGalleryView">
          Gallery View
        </button>
      </div>
    </div>
    <div class="grid-container bgColour">
      <div
        v-for="(item, index) in props.items"
        :key="index"
        class="grid-item-cont bgColour"
        :style="{ backgroundImage: `url(${item.imageURL})` }"
        @click="handleItemClick(item, $event)"
      >
        <div class="grid-item-details">
          <h1 class="textColour">{{ item.title }}</h1>
          <p class="textColour">{{ item.authors.join(', ') }}</p>
        </div>
      </div>
    </div>

    <div
      class="overlay"
      :class="{ active: selectedItem }"
      @click="handleItemClick(selectedItem)"
    ></div>

    <Teleport to="body" v-if="selectedItem">
      <div
        :class="[
          'bgColour',
          'textColour',
          'selected-item-container',
          selectedItem.animating ? 'animating' : '',
        ]"
        :style="selectedItemStyle"
      >
        <div
          class="selected-item-close textColour"
          @click="handleItemClick(selectedItem)"
        >
          <Icon name="material-symbols:close" size="2rem" />
        </div>
        <video
          :src="selectedItem.videoURL || '@/assets/video/000.mp4'"
          muted
          autoplay
          controls
          loop
        ></video>
        <div class="selected-item-details">
          <h1>{{ selectedItem.title }}</h1>
          <h3>{{ selectedItem.authors.join(', ') }}</h3>
          <p>{{ selectedItem.description }}</p>
        </div>
      </div>
    </Teleport>

    <DevOnly>
      <div
        style="position: fixed; top: 0; right: 0; z-index: 100; color: white"
      >
        {{ titleOpacity }}
        {{ isScrolledDown }}
        {{ devValue }}
      </div>
    </DevOnly>
  </div>
</template>

<script setup>
const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
});

const isScrolledDown = ref(false);
const titleOpacity = ref(1);

const handleScroll = (e) => {
  const scrollTop = e.target?.scrollTop || 0;
  // const percentScroll = 1 - scrollTop / (window.innerHeight / 2);

  const percentScroll =
    1 -
    scrollTop /
      parseFloat(
        window
          .getComputedStyle(document.querySelector('.grid-container'))
          .getPropertyValue('padding-top')
          .replace('px', '')
      );
  titleOpacity.value = percentScroll >= 0 ? percentScroll : 0;
};

const selectedItem = ref(null);
const clonedElement = ref(null);
const selectedItemStyle = ref({});

const handleItemClick = (item) => {
  if (selectedItem.value === item) {
    removeClone();
    selectedItem.value = null;
    return;
  }

  selectedItem.value = item;
  selectedItem.value.animating = true;
};

const removeClone = () => {
  if (clonedElement.value) {
    clonedElement.value.classList.remove('expanded');
    clonedElement.value.addEventListener('transitionend', () => {
      clonedElement.value?.remove();
      clonedElement.value = null;
    });
  }
};

const devValue = ref('Hello');

onMounted(() => {
  const scrollTop = document.querySelector('.grid-comp-cont').scrollTop;
  const percentScroll =
    1 -
    scrollTop /
      parseFloat(
        window
          .getComputedStyle(document.querySelector('.grid-container'))
          .getPropertyValue('padding-top')
          .replace('px', '')
      );
  titleOpacity.value = percentScroll >= 0 ? percentScroll : 0;
  devValue.value = 'Hello World';
});

const router = useRouter();

const changeToGalleryView = () => {
  console.log('Changing to gallery view');
  router.push({ query: { view: 'gallery' } });
};
</script>

<style>
.grid-comp-cont {
  height: 100vh;
  width: 100vw;
  overflow-y: scroll;
  position: fixed;
  inset: 0;
}

.title-cont {
  position: fixed;
  top: 0;
  left: 2rem;
  z-index: 10;
  pointer-events: none !important;
}

.title-cont h1 {
  font-family: 'Bigger Display', sans-serif;
  font-size: 20vh;
  margin: 0;
  transition: color 0.5s;
  text-transform: uppercase;
}

.title-cont h1:nth-child(1) {
  margin-bottom: -12vh;
}

.title-cont h1:nth-child(2) {
  margin-left: 40vh;
}

.title-cont .controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  position: absolute;
  left: 0;
  bottom: 10vh;
  padding: 1rem;
  height: 6rem;
  pointer-events: none;
}

.title-cont .controls .control {
  pointer-events: all;
}

.grid-container {
  position: relative;
  width: 100vw;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
  gap: 1rem;
  padding: 1rem;
  padding-top: 50vh;
  box-sizing: border-box;
}

.grid-item-cont {
  background-color: blueviolet;
  aspect-ratio: 4/5;
  background-position: center;
  background-size: cover;
  position: relative;
}

.grid-item-cont:hover .grid-item-details {
  opacity: 1;
}

.grid-item-details {
  padding: 1rem;
  position: absolute;
  bottom: 0;
  opacity: 0;
  transition: all 0.3s ease-out;
}

.grid-item-details h1 {
  font-size: 3rem;
  margin-bottom: -1rem;
  font-family: 'Bigger Display', sans-serif;
  text-transform: uppercase;
}

.grid-item-cont {
  position: relative;
  transition: all 0.3s ease-out;
  cursor: pointer;
}

.grid-item-cont.expanded {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80vw;
  height: 80vh;
  z-index: 1000;
}

.selected-item-container {
  position: fixed;
  transition: none;
  z-index: 1000;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  overflow-y: scroll;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 1rem 5vw;
}

.selected-item-container.animating {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  top: 50% !important;
  left: 50% !important;
  width: 80vw !important;
  height: 80vh !important;
  transform: translate(-50%, -50%) !important;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 999;
}

.overlay.active {
  opacity: 1;
  visibility: visible;
}

.selected-item-close {
  cursor: pointer;
  align-self: flex-end;
}

.selected-item-container video {
  width: 100%;
  height: auto;
  object-fit: contain;
}

.selected-item-details {
  max-width: 100%;
  padding: 1rem;
}

.selected-item-details h1 {
  font-size: 3rem;
  text-transform: uppercase;
  font-family: 'Bigger Display', sans-serif;
  margin-bottom: -1rem;
}

.selected-item-details h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

@media screen and (max-width: 768px) {
  .title-cont h1 {
    font-size: 10vh;
  }

  .title-cont h1:first-child {
    margin-bottom: -3rem;
  }

  .title-cont h1:last-child {
    margin-left: 10rem;
  }

  .grid-container {
    padding-top: 25vh;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  .grid-item-details h1 {
    font-size: 1.5rem;
    margin-bottom: -0.5rem;
  }

  .grid-item-details p {
    font-size: 0.8rem;
  }

  .selected-item-container {
    padding: 1rem 2vw;
  }

  .selected-item-details h1 {
    font-size: 2rem;
    margin-bottom: -0.5rem;
  }

  .selected-item-details h3 {
    font-size: 1rem;
    margin-bottom: 1rem;
  }

  .selected-item-details p {
    font-size: 0.8rem;
  }
}
</style>
