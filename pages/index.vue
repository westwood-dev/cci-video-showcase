<template>
  <div style="overflow: hidden">
    <Grid v-if="route.query.view == 'grid'" :items="items" />
    <Gallery v-else :items="items" />
    <!-- <TestGridGallery /> -->
  </div>
</template>
<script setup>
const route = useRoute();
const view = ref(route.query.view || 'gallery');

onMounted(() => {
  console.log(route.query);
});

const items = ref([]);

const exampleItem = {
  id: 1,
  title: 'Item 1',
  authors: ['Author 1', 'Author 2', 'Author 3'],
  description: `Lorem ipsum odor amet, consectetuer adipiscing elit. Maecenas sed hac dui venenatis ipsum per nullam condimentum. Est pulvinar hac faucibus cubilia; aliquam sapien penatibus eget lacinia. Curabitur himenaeos blandit maecenas class justo. Nisi eu dis feugiat volutpat proin; morbi aenean? Platea tincidunt orci etiam vulputate primis mauris scelerisque. Imperdiet porta sociosqu neque ultricies mauris porttitor.

Nascetur dui donec feugiat rhoncus quis suscipit praesent. Torquent conubia suspendisse commodo, phasellus facilisi dui. Risus mollis vestibulum lacus rutrum malesuada litora pulvinar. Ullamcorper porta aenean semper netus pulvinar euismod facilisi iaculis. Conubia cubilia ex dolor integer amet vestibulum. Pulvinar dignissim justo mattis ridiculus, mollis turpis hac odio orci. Magna facilisis consectetur vestibulum laoreet vivamus pharetra potenti placerat sagittis. Sit dignissim dapibus venenatis eleifend nisl. Eleifend fames quam diam molestie laoreet ornare aenean natoque.

Venenatis non maecenas tempor dictum bibendum sodales accumsan. Euismod magnis tempor montes hendrerit phasellus. Mattis scelerisque donec dis nulla sodales augue aenean eget morbi. Consequat commodo fames pulvinar, tempor ac rhoncus. Etiam torquent nullam interdum aptent duis. Arcu ad sollicitudin mauris suspendisse litora vivamus libero. Velit tempor praesent, fusce pretium nostra leo ac.

Sollicitudin ex quisque commodo, risus pretium arcu facilisi. Nisi risus quisque donec massa hendrerit justo aliquam. Proin euismod lacinia blandit eget massa dictumst ultrices ad. Aliquet lorem pulvinar dictum nisi ultricies cursus. Luctus dui condimentum justo arcu lorem. Ultrices commodo leo elit; velit varius porta. Risus a et convallis, sapien rhoncus senectus facilisis nulla. Massa maximus aenean magnis elementum nisi urna.

Penatibus netus aliquam tellus praesent duis vel. Posuere commodo elementum inceptos mattis habitant euismod. Egestas himenaeos augue tempor cras condimentum gravida cubilia pellentesque. Accumsan volutpat elit venenatis dis etiam blandit interdum. Molestie vitae hac congue ridiculus proin ante sed. Ipsum interdum auctor nec, tempor ante congue accumsan? Cubilia in eleifend netus iaculis auctor mus quisque. Nibh sociosqu fusce quis ipsum ante ornare. Dis ullamcorper neque tempus odio magnis. Ut bibendum phasellus pharetra imperdiet; suspendisse ex vestibulum tempor.`,
  imageURL: 'https://placehold.co/1280x720',
  videoURL: '/video/000.mp4',
};

for (let i = 0; i < 90; i++) {
  items.value.push({ ...exampleItem, id: i + 1, title: `Item ${i + 1}` });
}
</script>

<style scoped>
html {
  overflow: hidden;
}
</style>
