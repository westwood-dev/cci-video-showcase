<template>
  <div class="home-cont">
    <NuxtLink to="/one" class="brief-text-cont">
      <h1 class="textColour">brief one</h1>
      <h1 class="textColour" style="text-align: right">"light"</h1>
    </NuxtLink>
    <NuxtLink to="/two" class="brief-text-cont">
      <h1 class="textColour">brief two</h1>
      <h1 class="textColour" style="text-align: right">"behaviour"</h1>
    </NuxtLink>
  </div>
</template>

<script setup></script>

<style scoped>
html {
  overflow: hidden;
}
.home-cont {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
}

.brief-text-cont {
  padding: 2vw;
  background-color: rgb(var(--bg));
  transition: background-color 0.5s;
}

.brief-text-cont:hover {
  background-color: rgb(var(--text));
}

.brief-text-cont:hover h1 {
  color: rgb(var(--bg));
}

h1 {
  font-family: 'Bigger Display', sans-serif;
  text-transform: uppercase;
  font-size: 8vw;
  margin: 0;
  line-height: 8vw;
  width: 35vw;
}

@media screen and (max-width: 768px) {
  h1 {
    font-size: 20vw;
    line-height: 20vw;
    width: 90vw;
  }
}
</style>
