<template>
  <div class="grid-comp-cont bgColour" @scroll="handleScroll">
    <div class="title-cont textColour" :style="{ opacity: titleOpacity }">
      <h1>brief one</h1>
      <h1>"light"</h1>
    </div>
    <div class="grid-container bgColour">
      <div class="grid-item-cont">1</div>
      <div class="grid-item-cont">2</div>
      <div class="grid-item-cont">3</div>
      <div class="grid-item-cont">4</div>
      <div class="grid-item-cont">5</div>
      <div class="grid-item-cont">6</div>
      <div class="grid-item-cont">7</div>
      <div class="grid-item-cont">8</div>
      <div class="grid-item-cont">9</div>
      <div class="grid-item-cont">10</div>
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

const isScrolledDown = ref(false);
const titleOpacity = ref(1);

const handleScroll = (e) => {
  const scrollTop = e.target.scrollTop;
  const percentScroll = 1 - scrollTop / (window.innerHeight / 2);
  // console.log(percentScroll >= 0 ? percentScroll : 0);
  titleOpacity.value = percentScroll >= 0 ? percentScroll : 0;
  // isScrolledDown.value = e.target.scrollY > 0;
};
</script>

<style>
.grid-comp-cont {
  height: 100vh;
  overflow-y: scroll;
  position: relative;
}

.title-cont {
  position: fixed;
  top: 0;
  left: 0;
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
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  padding-top: 50vh;
}

.grid-item-cont {
  background-color: blueviolet;
  aspect-ratio: 3/5;
}
</style>
