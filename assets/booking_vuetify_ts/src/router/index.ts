// src/router/index.ts
import { createRouter, createWebHistory, Router } from 'vue-router';
import Index from '@/pages/index.vue';
import Calendar from '@/pages/Calendar.vue';
import Devices from '@/pages/Devices.vue';
import People from '@/pages/People.vue';


const routes = [
    { path: '/', component: Index },
    { path: '/calendar', component: Calendar, props: true
    },
    { path: '/devices', component: Devices },
    { path: '/people', component: People },
];


export function createAppRouter(base: string = '/'): Router {
    return createRouter({
        history: createWebHistory(base),
        routes,
    });
}
