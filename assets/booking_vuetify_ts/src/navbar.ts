/**
 * navbar.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import NavBar from './components/NavBar.vue'

// Composables
import { createApp } from 'vue'

import 'vuetify/dist/vuetify.min.css';


const app = createApp(NavBar)

registerPlugins(app)

app.mount('#navbar')
