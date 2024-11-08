<template>
  <div class="bgColour">
    <!-- <Gallery /> -->
    <NuxtPage />
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

@font-face {
  font-family: 'Bigger Display';
  src: url('@/assets/fonts/BiggerDisplay.woff') format('woff'),
    url('@/assets/fonts/BiggerDisplay.woff2') format('woff2');
}

html,
body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
  font-optical-sizing: auto;
  font-style: normal;
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

button {
  background-color: transparent;
  border: none;
  cursor: pointer;
}
</style>
