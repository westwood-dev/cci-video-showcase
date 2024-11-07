// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@nuxt/icon'],
  icon: {
    clientBundle: {
      icons: [
        'material-symbols:dark-mode',
        'material-symbols:light-mode',
        'material-symbols:close',
      ],
      scan: true,
    },
  },
  ssr: false,
  app: {
    head: {
      title: 'CCI Video Showcase',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          hid: 'description',
          name: 'description',
          content: 'Simple site to show video',
        },
      ],
      link: [{ rel: 'icon', type: 'image/svg', href: '/favicon.svg' }],
    },
    baseURL: '/cci-video-showcase/',
  },
});
