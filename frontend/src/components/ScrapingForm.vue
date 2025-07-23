<template>
  <div class="bg-white rounded-xl shadow-lg overflow-hidden">
    <!-- Form Section -->
    <div class="p-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">Website Scraping Configuration</h2>
      
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- URL Input -->
        <div>
          <label for="url" class="block text-sm font-medium text-gray-700 mb-2">
            Target URL *
          </label>
          <input
            id="url"
            v-model="formData.url"
            type="url"
            required
            placeholder="https://example.com"
            class="input-field"
            :disabled="isLoading"
          />
        </div>

        <!-- Login Toggle -->
        <div class="flex items-center">
          <input
            id="login-enabled"
            v-model="formData.login_enabled"
            type="checkbox"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            :disabled="isLoading"
          />
          <label for="login-enabled" class="ml-2 block text-sm text-gray-900">
            Require Login Authentication
          </label>
        </div>

        <!-- Login Fields -->
        <div v-if="formData.login_enabled" class="space-y-4 p-4 bg-gray-50 rounded-lg">
          <div>
            <label for="login-url" class="block text-sm font-medium text-gray-700 mb-2">
              Login URL *
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
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
                Username *
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
            
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                Password *
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
        <div class="flex justify-end">
          <button
            type="submit"
            :disabled="isLoading"
            class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <svg
              v-if="isLoading"
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
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
            <span>{{ isLoading ? 'Scraping...' : 'Start Scraping' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'

export default {
  name: 'ScrapingForm',
  props: {
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['submit'],
  setup(props, { emit }) {
    const formData = reactive({
      url: '',
      login_enabled: false,
      login_url: '',
      username: '',
      password: ''
    })

    const handleSubmit = () => {
      emit('submit', { ...formData })
    }

    return {
      formData,
      handleSubmit
    }
  }
}
</script> 