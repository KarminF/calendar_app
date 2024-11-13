/**
 * navbar.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import NavBarInstance from './components/NavBarInstance.vue';

// Composables
import { createApp } from 'vue'

import 'vuetify/dist/vuetify.min.css';


const app = createApp(NavBarInstance)

registerPlugins(app)

app.mount('#navbar')
