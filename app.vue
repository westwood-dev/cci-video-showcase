<template>
  <div>
    <!-- <Gallery /> -->
    <NuxtPage />
  </div>
</template>

<style>
@font-face {
  font-family: 'Bigger Display';
  src: url('@/assets/fonts/BiggerDisplay.otf') format('opentype');
}

:root {
  --text: 255, 255, 255;
  --bg: 0, 0, 0;
}

.textColour {
  color: rgb(var(--text));
  transition: color 0.5s;
}

.bgColour {
  background-color: rgb(var(--bg));
  transition: background-color 0.5s;
}

.textColourInvert {
  color: rgb(var(--bg));
  transition: color 0.5s;
}

.bgColourInvert {
  background-color: rgb(var(--text));
  transition: background-color 0.5s;
}
</style>
