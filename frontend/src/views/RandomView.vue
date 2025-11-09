<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="sm:flex sm:items-center sm:justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">随机选题</h1>
        <p class="mt-2 text-gray-600">随机选择题目，支持按类别和难度筛选</p>
      </div>
    </div>

    <!-- 选题参数配置 -->
    <Card class="mb-8">
      <h2 class="text-lg font-semibold text-gray-900 mb-6">选题参数</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 题目数量 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            选题数量 *
          </label>
          <select v-model="randomParams.count" class="select" required>
            <option value="">请选择数量</option>
            <option v-for="n in [1, 2, 3, 4, 5, 10, 15, 20, 25, 30]" :key="n" :value="n">
              {{ n }} 题
            </option>
          </select>
        </div>

        <!-- 类别筛选 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            题目类别（可选）
          </label>
          <div class="max-h-32 overflow-y-auto border border-gray-300 rounded-md p-2">
            <div v-for="category in categories" :key="category.value" class="mb-1">
              <label class="flex items-center">
                <input
                  type="checkbox"
                  :value="category.value"
                  v-model="selectedCategories"
                  class="mr-2"
                />
                <span class="text-sm">{{ category.label }}</span>
              </label>
            </div>
          </div>
        </div>

        <!-- 难度筛选 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            难度等级（可选）
          </label>
          <div class="max-h-32 overflow-y-auto border border-gray-300 rounded-md p-2">
            <div v-for="difficulty in difficulties" :key="difficulty.value" class="mb-1">
              <label class="flex items-center">
                <input
                  type="checkbox"
                  :value="difficulty.value"
                  v-model="selectedDifficulties"
                  class="mr-2"
                />
                <span class="text-sm">{{ difficulty.label }}</span>
              </label>
            </div>
          </div>
        </div>

        <!-- 快速选择 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            快速选择
          </label>
          <div class="space-y-2">
            <Button
              variant="secondary"
              size="sm"
              class="w-full"
              @click="selectAllCategories"
            >
              全选类别
            </Button>
            <Button
              variant="secondary"
              size="sm"
              class="w-full"
              @click="selectAllDifficulties"
            >
              全选难度
            </Button>
            <Button
              variant="secondary"
              size="sm"
              class="w-full"
              @click="clearAllSelections"
            >
              清除选择
            </Button>
          </div>
        </div>
      </div>

      <div class="mt-6 flex justify-end space-x-3">
        <Button
          variant="secondary"
          @click="clearAll"
        >
          重置参数
        </Button>
        <Button
          variant="primary"
          :loading="selecting"
          :disabled="!randomParams.count"
          @click="generateRandomQuestions"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          随机选题
        </Button>
      </div>
    </Card>

    <!-- 选中的题目列表 -->
    <div v-if="selectedQuestions.length > 0">
      <div class="sm:flex sm:items-center sm:justify-between mb-6">
        <h2 class="text-xl font-semibold text-gray-900">
          已选题目 ({{ selectedQuestions.length }})
        </h2>
        <div class="mt-4 sm:mt-0 flex space-x-3">
          <Button
            variant="secondary"
            @click="exportQuestions"
          >
            导出题目
          </Button>
          <Button
            variant="primary"
            @click="startInterviewMode"
            :disabled="selectedQuestions.length === 0"
          >
            开始面试
          </Button>
        </div>
      </div>

      <div class="space-y-4">
        <Card
          v-for="(question, index) in selectedQuestions"
          :key="question.id"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center mb-3">
                <span class="text-sm text-gray-500 mr-3">#{{ index + 1 }}</span>
                <h3 class="text-lg font-semibold text-gray-900 mr-3">
                  {{ question.title }}
                </h3>
                <DifficultyBadge :difficulty="question.difficulty" class="mr-2" />
                <CategoryBadge :category="question.category" />
              </div>
              
              <div class="mb-4">
                <MarkdownRenderer :content="question.content" />
              </div>

              <div v-if="showAnalysis && question.analysis" class="mb-4">
                <h4 class="text-sm font-medium text-gray-700 mb-2">解题思路</h4>
                <MarkdownRenderer :content="question.analysis" />
              </div>

              <div v-if="question.tags.length > 0" class="flex items-center text-sm text-gray-500">
                标签: 
                <span v-for="tag in question.tags" :key="tag" class="inline-block bg-gray-100 rounded px-2 py-1 text-xs mr-1 ml-1">
                  {{ tag }}
                </span>
              </div>
            </div>
            
            <div class="flex items-center space-x-2 ml-4">
              <Button
                variant="secondary"
                size="sm"
                @click="toggleAnalysis"
              >
                {{ showAnalysis ? '隐藏解析' : '显示解析' }}
              </Button>
              <Button
                variant="danger"
                size="sm"
                @click="removeQuestion(index)"
              >
                移除
              </Button>
            </div>
          </div>
        </Card>
      </div>

      <!-- 重新选择 -->
      <div class="mt-8 text-center">
        <Button
          variant="secondary"
          @click="reselectQuestions"
        >
          重新选择题目
        </Button>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">开始随机选题</h3>
      <p class="mt-1 text-sm text-gray-500">设置选题参数，然后点击随机选题按钮</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionStore } from '@/stores'
import { categories, difficulties } from '@/types'
import type { Question } from '@/types'
import Card from '@/components/common/Card.vue'
import Button from '@/components/common/Button.vue'
import DifficultyBadge from '@/components/common/DifficultyBadge.vue'
import CategoryBadge from '@/components/common/CategoryBadge.vue'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'

const router = useRouter()
const questionStore = useQuestionStore()

const randomParams = ref({
  count: 5 as number | '',
})

const selectedCategories = ref<string[]>([])
const selectedDifficulties = ref<string[]>([])
const selectedQuestions = ref<Question[]>([])
const selecting = ref(false)
const showAnalysis = ref(false)

const selectAllCategories = () => {
  selectedCategories.value = categories.map(c => c.value)
}

const selectAllDifficulties = () => {
  selectedDifficulties.value = difficulties.map(d => d.value)
}

const clearAllSelections = () => {
  selectedCategories.value = []
  selectedDifficulties.value = []
}

const clearAll = () => {
  randomParams.value.count = ''
  selectedCategories.value = []
  selectedDifficulties.value = []
  selectedQuestions.value = []
}

const generateRandomQuestions = async () => {
  if (!randomParams.value.count) return
  
  selecting.value = true
  try {
    const params: any = {
      count: randomParams.value.count
    }
    
    if (selectedCategories.value.length > 0) {
      params.categories = selectedCategories.value
    }
    
    if (selectedDifficulties.value.length > 0) {
      params.difficulties = selectedDifficulties.value
    }
    
    const response = await questionStore.getRandomQuestions(params)
    selectedQuestions.value = response
  } catch (error) {
    console.error('选题失败:', error)
  } finally {
    selecting.value = false
  }
}

const removeQuestion = (index: number) => {
  selectedQuestions.value.splice(index, 1)
}

const toggleAnalysis = () => {
  showAnalysis.value = !showAnalysis.value
}

const reselectQuestions = () => {
  selectedQuestions.value = []
  generateRandomQuestions()
}

const exportQuestions = () => {
  if (selectedQuestions.value.length === 0) return
  
  const exportData = {
    questions: selectedQuestions.value,
    exportTime: new Date().toISOString(),
    totalCount: selectedQuestions.value.length
  }
  
  const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `questions_${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const startInterviewMode = () => {
  if (selectedQuestions.value.length === 0) return
  
  // 将选中的题目传递给面试模式
  const interviewStore = useInterviewStore()
  interviewStore.startSession(selectedQuestions.value)
  router.push('/interview')
}

// 添加导入InterviewStore
import { useInterviewStore } from '@/stores'
</script>