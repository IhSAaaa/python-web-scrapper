<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 relative overflow-hidden">
    <!-- Background Pattern -->
    <div class="absolute inset-0 bg-grid-pattern opacity-5"></div>
    
    <!-- Floating Elements -->
    <div class="absolute top-20 left-10 w-72 h-72 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
    <div class="absolute top-40 right-10 w-72 h-72 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse" style="animation-delay: 2s;"></div>
    
    <!-- Header -->
    <header class="relative z-10 backdrop-blur-md bg-white/70 border-b border-white/20">
      <div class="max-w-6xl mx-auto px-6 py-6">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c-5 0-9-4-9-9s4-9 9-9"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                Web Scraper
              </h1>
              <p class="text-sm text-gray-500 font-medium">Intelligent Data Extraction</p>
            </div>
          </div>
          <div class="hidden md:flex items-center space-x-2 text-sm text-gray-500">
            <span class="px-3 py-1 bg-white/50 rounded-full backdrop-blur-sm">Vue 3</span>
            <span class="px-3 py-1 bg-white/50 rounded-full backdrop-blur-sm">FastAPI</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="relative z-10 max-w-4xl mx-auto px-6 py-12">
      <!-- Main Card -->
      <div class="backdrop-blur-xl bg-white/80 rounded-3xl shadow-2xl border border-white/20 overflow-hidden">
        <!-- Form Section -->
        <div class="p-8 md:p-12">
          <div class="text-center mb-8">
            <h2 class="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-2">
              Website Scraping
            </h2>
            <p class="text-gray-600 text-lg">Extract links and images from any website with ease</p>
          </div>
          
          <form @submit.prevent="handleSubmit" class="space-y-8">
            <!-- URL Input -->
            <div class="space-y-2">
              <label for="url" class="block text-sm font-semibold text-gray-700">
                Target URL
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c-5 0-9-4-9-9s4-9 9-9"></path>
                  </svg>
                </div>
                <input
                  id="url"
                  v-model="formData.url"
                  type="url"
                  required
                  placeholder="https://example.com"
                  class="input-field pl-12"
                  :disabled="isLoading"
                />
              </div>
            </div>

            <!-- Login Toggle -->
            <div class="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-blue-50 rounded-2xl border border-gray-100">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-900">Authentication Required</h3>
                  <p class="text-sm text-gray-600">Enable if the website requires login</p>
                </div>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input
                  v-model="formData.login_enabled"
                  type="checkbox"
                  class="sr-only peer"
                  :disabled="isLoading"
                />
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gradient-to-r peer-checked:from-blue-500 peer-checked:to-purple-500"></div>
              </label>
            </div>

            <!-- Login Fields -->
            <div v-if="formData.login_enabled" class="space-y-6 p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl border border-blue-100">
              <div class="space-y-2">
                <label for="login-url" class="block text-sm font-semibold text-gray-700">
                  Login URL
                </label>
                <input
                  id="login-url"
                  v-model="formData.login_url"
                  type="url"
                  placeholder="https://example.com/login"
                  class="input-field"
                  :disabled="isLoading"
                />
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="space-y-2">
                  <label for="username" class="block text-sm font-semibold text-gray-700">
                    Username
                  </label>
                  <input
                    id="username"
                    v-model="formData.username"
                    type="text"
                    placeholder="Enter username"
                    class="input-field"
                    :disabled="isLoading"
                  />
                </div>
                
                <div class="space-y-2">
                  <label for="password" class="block text-sm font-semibold text-gray-700">
                    Password
                  </label>
                  <input
                    id="password"
                    v-model="formData.password"
                    type="password"
                    placeholder="Enter password"
                    class="input-field"
                    :disabled="isLoading"
                  />
                </div>
              </div>
            </div>

            <!-- Submit Button -->
            <div class="flex justify-center pt-4">
              <button
                type="submit"
                :disabled="isLoading"
                class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-3 px-8 py-4 text-lg font-semibold rounded-2xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
              >
                <svg
                  v-if="isLoading"
                  class="animate-spin h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                <svg
                  v-else
                  class="h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
                <span>{{ isLoading ? 'Scraping in Progress...' : 'Start Scraping' }}</span>
              </button>
            </div>
          </form>
        </div>

        <!-- Results Section -->
        <div v-if="results" class="border-t border-gray-100 p-8 md:p-12 bg-gradient-to-br from-green-50 to-emerald-50">
          <div class="text-center mb-8">
            <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-2">Scraping Completed!</h3>
            <p class="text-gray-600">{{ results.message }}</p>
          </div>
          
          <!-- Statistics Cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-lg">
              <div class="flex items-center">
                <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mr-4">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-600">Links Found</p>
                  <p class="text-3xl font-bold text-gray-900">{{ results.links_count }}</p>
                </div>
              </div>
            </div>

            <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-lg">
              <div class="flex items-center">
                <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mr-4">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-600">Images Downloaded</p>
                  <p class="text-3xl font-bold text-gray-900">{{ results.images_count }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Session Info -->
          <div v-if="results.session_id" class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-6 border border-blue-100 mb-6">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div>
                  <p class="font-semibold text-gray-900">Session ID: {{ results.session_id }}</p>
                  <p class="text-sm text-gray-600">Files available for 24 hours</p>
                </div>
              </div>
              <div v-if="results.expires_at" class="text-right">
                <p class="text-sm font-medium text-gray-900">Expires at</p>
                <p class="text-sm text-gray-600">{{ formatExpiryTime(results.expires_at) }}</p>
              </div>
            </div>
          </div>

          <!-- Download Section -->
          <div class="space-y-4">
            <h4 class="text-lg font-semibold text-gray-900 text-center mb-6">Download Your Results</h4>
            
            <div v-if="results.excel_file" class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-lg hover:shadow-xl transition-shadow duration-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-gradient-to-r from-green-500 to-green-600 rounded-xl flex items-center justify-center mr-4">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900">Links CSV File</p>
                    <p class="text-sm text-gray-600">Download all extracted links</p>
                  </div>
                </div>
                <a
                  :href="getFullUrl(results.excel_file)"
                  download
                  class="btn-primary flex items-center space-x-2 px-6 py-3 rounded-xl"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  <span>Download CSV</span>
                </a>
              </div>
            </div>

            <div v-if="results.images_folder" class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-white/20 shadow-lg hover:shadow-xl transition-shadow duration-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mr-4">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                    </svg>
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900">Images Collection</p>
                    <p class="text-sm text-gray-600">Download all extracted images</p>
                  </div>
                </div>
                <a
                  :href="getFullUrl(results.images_folder)"
                  target="_blank"
                  class="btn-secondary flex items-center space-x-2 px-6 py-3 rounded-xl"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  <span>Download Images</span>
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Error Section -->
        <div v-if="error" class="border-t border-gray-100 p-8 md:p-12 bg-gradient-to-br from-red-50 to-pink-50">
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-red-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Oops! Something went wrong</h3>
            <p class="text-gray-600 mb-4">{{ error }}</p>
            <button
              @click="error = null"
              class="btn-primary px-6 py-3 rounded-xl"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import axios from 'axios'

// Configure axios base URL for backend API
const getApiBaseUrl = () => {
  // Check environment variables
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }
  
  // Check if running in Docker container
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8001'
  }
  
  // Default fallback
  return '/api'
}

const API_BASE_URL = getApiBaseUrl()
axios.defaults.baseURL = API_BASE_URL

// Log API configuration for debugging
console.log('API Base URL:', API_BASE_URL)
console.log('Environment:', import.meta.env.MODE)

export default {
  name: 'App',
  setup() {
    const isLoading = ref(false)
    const results = ref(null)
    const error = ref(null)

    const formData = reactive({
      url: '',
      login_enabled: false,
      login_url: '',
      username: '',
      password: ''
    })

    const getFullUrl = (relativeUrl) => {
      if (!relativeUrl) return ''
      
      // If URL is already absolute, return as is
      if (relativeUrl.startsWith('http://') || relativeUrl.startsWith('https://')) {
        return relativeUrl
      }
      
      // If URL starts with /, it's a relative URL from backend
      if (relativeUrl.startsWith('/')) {
        const fullUrl = `${API_BASE_URL}${relativeUrl}`
        console.log(`Converting relative URL: ${relativeUrl} -> ${fullUrl}`)
        return fullUrl
      }
      
      // Otherwise, assume it's relative to current domain
      return relativeUrl
    }

    const formatExpiryTime = (expiryTime) => {
      if (!expiryTime) return ''
      
      try {
        const expiryDate = new Date(expiryTime)
        const now = new Date()
        const diffHours = Math.max(0, Math.floor((expiryDate - now) / (1000 * 60 * 60)))
        const diffMinutes = Math.max(0, Math.floor((expiryDate - now) / (1000 * 60)) % 60)
        
        if (diffHours > 0) {
          return `${diffHours}h ${diffMinutes}m remaining`
        } else {
          return `${diffMinutes}m remaining`
        }
      } catch (error) {
        console.error('Error formatting expiry time:', error)
        return 'Unknown'
      }
    }

    const handleSubmit = async () => {
      isLoading.value = true
      error.value = null
      results.value = null

      try {
        const response = await axios.post('/api/scrape', formData)
        results.value = response.data
      } catch (err) {
        console.error('Scraping error:', err)
        error.value = err.response?.data?.detail || err.message || 'An error occurred'
      } finally {
        isLoading.value = false
      }
    }

    return {
      isLoading,
      results,
      error,
      formData,
      handleSubmit,
      getFullUrl,
      formatExpiryTime
    }
  }
}
</script> 