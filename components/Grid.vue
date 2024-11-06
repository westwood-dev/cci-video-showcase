<template>
  <div class="grid-comp-cont bgColour" @scroll="handleScroll">
    <div class="title-cont textColour" :style="{ opacity: titleOpacity }">
      <h1>brief one</h1>
      <h1>"light"</h1>
    </div>
    <div class="grid-container bgColour">
      <div
        v-for="(item, index) in props.items"
        :key="index"
        class="grid-item-cont bgColour"
        :style="{ backgroundImage: `url(${item.imageURL})` }"
      >
        <div class="grid-item-details">
          <h1 class="textColour">{{ item.title }}</h1>
          <p class="textColour">{{ item.authors.join(', ') }}</p>
        </div>
      </div>
    </div>
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
  // console.log(percentScroll >= 0 ? percentScroll : 0);
  titleOpacity.value = percentScroll >= 0 ? percentScroll : 0;
  // isScrolledDown.value = e.target.scrollY > 0;
};

const devValue = ref('Hello');
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
}

.title-cont h1 {
  font-family: 'Bigger Display', sans-serif;
  font-size: 20vh;
  margin: 0;
  transition: color 0.5s;
  text-transform: uppercase;
}

.title-cont h1:first-child {
  margin-bottom: -5rem;
}

.title-cont h1:last-child {
  margin-left: 20rem;
}

.grid-container {
  width: 100vw;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
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

.grid-item-details {
  padding: 1rem;
  position: absolute;
  bottom: 0;
}

.grid-item-details h1 {
  font-size: 3rem;
  margin-bottom: -1rem;
  font-family: 'Bigger Display', sans-serif;
  text-transform: uppercase;
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
}
</style>
