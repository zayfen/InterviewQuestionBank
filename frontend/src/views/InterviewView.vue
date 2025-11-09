<template>
  <!-- 全屏面试模式 -->
  <div v-if="interviewStore.sessionActive" class="fixed inset-0 bg-gray-900 z-50 flex flex-col">
    <!-- 顶部导航 -->
    <div class="bg-gray-800 text-white px-6 py-4 flex items-center justify-between">
      <div class="flex items-center">
        <h1 class="text-xl font-bold">面试模式</h1>
        <div class="ml-6 flex items-center space-x-4">
          <span class="text-sm">
            第 {{ interviewStore.currentIndex + 1 }} / {{ interviewStore.totalQuestions }} 题
          </span>
          <DifficultyBadge :difficulty="currentQuestion?.difficulty" />
          <CategoryBadge :category="currentQuestion?.category" />
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <Button
          variant="secondary"
          size="sm"
          @click="toggleFullScreen"
        >
          {{ isFullScreen ? '退出全屏' : '全屏' }}
        </Button>
        <Button
          variant="danger"
          size="sm"
          @click="confirmEndInterview"
        >
          结束面试
        </Button>
      </div>
    </div>

    <!-- 进度条 -->
    <div class="bg-gray-700 px-6 py-2">
      <div class="w-full bg-gray-600 rounded-full h-2">
        <div
          class="bg-primary-600 h-2 rounded-full transition-all duration-300"
          :style="{ width: `${interviewStore.progress}%` }"
        ></div>
      </div>
    </div>

    <!-- 题目内容区域 -->
    <div class="flex-1 bg-white overflow-y-auto">
      <div class="max-w-4xl mx-auto p-8">
        <div v-if="currentQuestion" class="space-y-8">
          <!-- 题目标题 -->
          <div class="text-center">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">
              {{ currentQuestion.title }}
            </h2>
          </div>

          <!-- 题目内容 -->
          <div class="prose prose-lg max-w-none">
            <MarkdownRenderer :content="currentQuestion.content" />
          </div>

          <!-- 解析切换按钮 -->
          <div class="text-center">
            <Button
              variant="secondary"
              @click="interviewStore.toggleAnalysis"
            >
              {{ interviewStore.showAnalysis ? '隐藏解析' : '显示解析' }}
            </Button>
          </div>

          <!-- 解题思路 -->
          <div v-if="interviewStore.showAnalysis && currentQuestion.analysis" class="bg-blue-50 rounded-lg p-6">
            <h3 class="text-lg font-semibold text-blue-900 mb-4">解题思路</h3>
            <div class="prose prose-blue max-w-none">
              <MarkdownRenderer :content="currentQuestion.analysis" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <div class="bg-gray-800 px-6 py-4 flex items-center justify-between">
      <Button
        variant="secondary"
        :disabled="interviewStore.currentIndex === 0"
        @click="interviewStore.previousQuestion"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
        上一题
      </Button>

      <div class="text-white text-center">
        <div class="text-sm text-gray-300">进度</div>
        <div class="text-lg font-semibold">
          {{ Math.round(interviewStore.progress) }}%
        </div>
      </div>

      <Button
        variant="primary"
        :disabled="interviewStore.currentIndex >= interviewStore.totalQuestions - 1"
        @click="interviewStore.nextQuestion"
      >
        下一题
        <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
        </svg>
      </Button>
    </div>
  </div>

  <!-- 配置页面 -->
  <div v-else class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="sm:flex sm:items-center sm:justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">面试模式</h1>
        <p class="mt-2 text-gray-600">模拟真实面试场景，按难度梯度展示题目</p>
      </div>
    </div>

    <!-- 快速开始 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <Card
        v-for="preset in presets"
        :key="preset.id"
        class="hover:shadow-lg transition-shadow cursor-pointer"
        @click="startPresetInterview(preset.id)"
      >
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900">{{ preset.name }}</h3>
            <div class="text-2xl">{{ preset.icon }}</div>
          </div>
        </template>
        <p class="text-gray-600 mb-4">{{ preset.description }}</p>
        <div class="text-sm text-gray-500">
          <div>简单: {{ preset.easy }} 题</div>
          <div>中等: {{ preset.medium }} 题</div>
          <div>困难: {{ preset.hard }} 题</div>
        </div>
      </Card>
    </div>

    <!-- 自定义配置 -->
    <Card>
      <h2 class="text-lg font-semibold text-gray-900 mb-6">自定义面试</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            简单题目数量
          </label>
          <select v-model="customConfig.easy_count" class="select">
            <option v-for="n in 10" :key="n" :value="n - 1">
              {{ n - 1 }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            中等题目数量
          </label>
          <select v-model="customConfig.medium_count" class="select">
            <option v-for="n in 11" :key="n" :value="n - 1">
              {{ n - 1 }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            困难题目数量
          </label>
          <select v-model="customConfig.hard_count" class="select">
            <option v-for="n in 11" :key="n" :value="n - 1">
              {{ n - 1 }}
            </option>
          </select>
        </div>
      </div>

      <div class="text-center text-sm text-gray-500 mb-6">
        总计：{{ totalQuestions }} 题
      </div>

      <div class="flex justify-center">
        <Button
          variant="primary"
          :loading="loading"
          :disabled="totalQuestions === 0"
          @click="startCustomInterview"
        >
          开始自定义面试
        </Button>
      </div>
    </Card>
  </div>

  <!-- 结束面试确认模态框 -->
  <Modal
    :show="showEndConfirm"
    title="确认结束面试"
    @update:show="showEndConfirm = $event"
  >
    <p class="text-gray-600">
      确定要结束当前面试吗？您的进度将会丢失。
    </p>
    
    <template #footer>
      <Button variant="danger" @click="endInterview">
        确认结束
      </Button>
      <Button variant="secondary" @click="showEndConfirm = false">
        取消
      </Button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useInterviewStore } from '@/stores'
import { useQuestionStore } from '@/stores'
import type { Question } from '@/types'
import Button from '@/components/common/Button.vue'
import Card from '@/components/common/Card.vue'
import Modal from '@/components/common/Modal.vue'
import DifficultyBadge from '@/components/common/DifficultyBadge.vue'
import CategoryBadge from '@/components/common/CategoryBadge.vue'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'

const interviewStore = useInterviewStore()
const questionStore = useQuestionStore()

const loading = ref(false)
const isFullScreen = ref(false)
const showEndConfirm = ref(false)

const customConfig = ref({
  easy_count: 2,
  medium_count: 3,
  hard_count: 1
})

const totalQuestions = computed(() => {
  return customConfig.value.easy_count + customConfig.value.medium_count + customConfig.value.hard_count
})

const currentQuestion = computed(() => interviewStore.currentQuestion)

const presets = [
  {
    id: 'quick',
    name: '快速面试',
    icon: '⚡',
    description: '适合初筛，包含基础到中等难度题目',
    easy: 2,
    medium: 2,
    hard: 1
  },
  {
    id: 'standard',
    name: '标准面试',
    icon: '🎯',
    description: '标准技术面试，涵盖各难度层次',
    easy: 3,
    medium: 4,
    hard: 2
  },
  {
    id: 'comprehensive',
    name: '综合面试',
    icon: '📚',
    description: '深度技术面试，适合高级工程师',
    easy: 5,
    medium: 5,
    hard: 3
  }
]

onMounted(() => {
  // 检查是否有从随机选题页面传递的题目
  if (interviewStore.sessionQuestions.length > 0) {
    return
  }
  
  // 如果没有预设题目，加载一些题目作为示例
  loadSampleQuestions()
})

const loadSampleQuestions = async () => {
  try {
    await questionStore.fetchQuestions({ page: 1, size: 10 })
  } catch (error) {
    console.error('加载题目失败:', error)
  }
}

const startPresetInterview = async (presetId: string) => {
  loading.value = true
  try {
    const preset = presets.find(p => p.id === presetId)
    if (!preset) return

    const response = await questionStore.getPresetInterview(presetId)
    if (response && response.items && response.items.length > 0) {
      interviewStore.startSession(response.items)
    }
  } catch (error) {
    console.error('开始预设面试失败:', error)
  } finally {
    loading.value = false
  }
}

const startCustomInterview = async () => {
  if (totalQuestions.value === 0) return
  
  loading.value = true
  try {
    const response = await questionStore.createInterviewSession(customConfig.value)
    if (response && response.items && response.items.length > 0) {
      interviewStore.startSession(response.items)
    }
  } catch (error) {
    console.error('开始自定义面试失败:', error)
  } finally {
    loading.value = false
  }
}

const toggleFullScreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    isFullScreen.value = true
  } else {
    document.exitFullscreen()
    isFullScreen.value = false
  }
}

const confirmEndInterview = () => {
  showEndConfirm.value = true
}

const endInterview = () => {
  interviewStore.endSession()
  showEndConfirm.value = false
  isFullScreen.value = false
}
</script>