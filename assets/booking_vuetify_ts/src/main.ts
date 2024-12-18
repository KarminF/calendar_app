/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

import { createAppRouter } from './router';

import 'vuetify/dist/vuetify.min.css';

const app = createApp(App)

const router = createAppRouter('/booking');

app.use(router);

registerPlugins(app)

app.mount('#app')
