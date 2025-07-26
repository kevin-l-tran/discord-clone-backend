import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import Groups from './Groups.vue'
import grouprouter from './groups-router'

const app = createApp(Groups)

app.use(createPinia())
app.use(grouprouter)

app.mount('#groups-app')
