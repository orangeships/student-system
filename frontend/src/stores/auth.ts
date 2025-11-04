import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const user = ref<any>(null)

  const login = async (credentials: { username: string; password: string }) => {
    // Mock login - in real app, this would call your auth API
    token.value = 'mock-token'
    user.value = { id: 1, username: credentials.username }
  }

  const logout = () => {
    token.value = null
    user.value = null
  }

  const isAuthenticated = computed(() => !!token.value)

  return {
    token,
    user,
    login,
    logout,
    isAuthenticated
  }
})