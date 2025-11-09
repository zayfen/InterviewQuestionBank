<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-xl font-bold text-gray-900">面试题库管理系统</h1>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                to="/"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-700"
                :class="{ 'border-b-2 border-primary-500': $route.path === '/' }"
              >
                首页
              </router-link>
              <router-link
                to="/questions"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-700"
                :class="{ 'border-b-2 border-primary-500': $route.path === '/questions' }"
              >
                题目管理
              </router-link>
              <router-link
                to="/generate"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-700"
                :class="{ 'border-b-2 border-primary-500': $route.path === '/generate' }"
              >
                AI生成
              </router-link>
              <router-link
                to="/random"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-700"
                :class="{ 'border-b-2 border-primary-500': $route.path === '/random' }"
              >
                随机选题
              </router-link>
              <router-link
                to="/interview"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-700"
                :class="{ 'border-b-2 border-primary-500': $route.path === '/interview' }"
              >
                面试模式
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
// App component
</script>