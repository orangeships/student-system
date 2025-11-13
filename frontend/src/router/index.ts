import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Layout from '@/components/Layout.vue'
import HomeView from '@/views/HomeView.vue'
import TransactionsView from '@/views/TransactionsView.vue'
import CategoriesView from '@/views/CategoriesView.vue'
import BudgetView from '@/views/BudgetView.vue'
import GoalsView from '@/views/GoalsView.vue'
import LoginView from '@/views/LoginView.vue'
import ApiTestView from '@/views/ApiTestView.vue'
import TestConnectionView from '@/views/TestConnectionView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/test-connection',
      name: 'test-connection',
      component: TestConnectionView,
    },
    {
      path: '/',
      component: Layout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView,
        },
        {
          path: '/transactions',
          name: 'transactions',
          component: TransactionsView,
        },
        {
          path: '/categories',
          name: 'categories',
          component: CategoriesView,
        },
        {
          path: '/budget',
          name: 'budget',
          component: BudgetView,
        },
        {
          path: '/goals',
          name: 'goals',
          component: GoalsView,
        },
        {
          path: '/api-test',
          name: 'api-test',
          component: ApiTestView,
        },
      ],
    },
  ],
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
