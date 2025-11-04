import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout.vue'
import HomeView from '@/views/HomeView.vue'
import TransactionsView from '@/views/TransactionsView.vue'
import CategoriesView from '@/views/CategoriesView.vue'
import BudgetView from '@/views/BudgetView.vue'
import GoalsView from '@/views/GoalsView.vue'

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
      ],
    },
  ],
})

export default router
