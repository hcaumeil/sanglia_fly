import './assets/main.css'

import { createApp } from 'vue'
// @ts-ignore can't resolve type
import App from './App.vue'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import 'leaflet/dist/leaflet.css';

const app = createApp(App)

const vuetify = createVuetify({
    components,
    directives,
})

app.use(vuetify);

app.mount('#app')
