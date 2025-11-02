import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
        },
        {
          path: '/students',
          name: 'students',
          component: () => import('@/views/StudentsView.vue'),
        },
        {
          path: '/finance',
          name: 'finance',
          component: () => import('@/views/FinanceView.vue'),
        },
        {
          path: '/statistics',
          name: 'statistics',
          component: () => import('@/views/StatisticsView.vue'),
        },
      ],
    },
  ],
})

export default router
