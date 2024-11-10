// src/router/index.ts
import { createRouter, createWebHistory, Router } from 'vue-router';
import Index from '@/pages/index.vue';
import Calendar from '@/pages/Calendar.vue';

const routes = [
    { path: '/', component: Index },
    { path: '/calendar', component: Calendar },
];

/**
 * 创建一个 Vue Router 实例
 * @param base - 路由的基础路径
 * @returns Vue Router 实例
 */
export function createAppRouter(base: string = '/'): Router {
    return createRouter({
        history: createWebHistory(base),
        routes,
    });
}
