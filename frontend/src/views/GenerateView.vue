<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="sm:flex sm:items-center sm:justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">AI题目生成</h1>
        <p class="mt-2 text-gray-600">使用AI技术自动生成高质量的面试题目</p>
      </div>
    </div>

    <!-- 生成参数配置 -->
    <Card class="mb-8">
      <h2 class="text-lg font-semibold text-gray-900 mb-6">生成参数</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            题目类别 *
          </label>
          <select v-model="generateParams.category" class="select" required>
            <option value="">请选择类别</option>
            <option v-for="category in categories" :key="category.value" :value="category.value">
              {{ category.label }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            难度等级 *
          </label>
          <select v-model="generateParams.difficulty" class="select" required>
            <option value="">请选择难度</option>
            <option v-for="difficulty in difficulties" :key="difficulty.value" :value="difficulty.value">
              {{ difficulty.label }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            生成数量 *
          </label>
          <select v-model="generateParams.count" class="select" required>
            <option value="">请选择数量</option>
            <option v-for="n in [1, 2, 3, 4, 5]" :key="n" :value="n">
              {{ n }} 题
            </option>
          </select>
        </div>
      </div>
      
      <div class="mt-6 flex justify-end">
        <Button
          variant="primary"
          :loading="generating"
          :disabled="!isFormValid"
          @click="generateQuestions"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
          </svg>
          生成题目
        </Button>
      </div>
    </Card>

    <!-- 生成的题目列表 -->
    <div v-if="generatedQuestions.length > 0">
      <div class="sm:flex sm:items-center sm:justify-between mb-6">
        <h2 class="text-xl font-semibold text-gray-900">生成的题目</h2>
        <div class="mt-4 sm:mt-0 flex space-x-3">
          <Button
            variant="secondary"
            @click="regenerateQuestions"
            :loading="generating"
          >
            重新生成
          </Button>
          <Button
            variant="primary"
            @click="saveAllQuestions"
            :loading="saving"
            :disabled="savedQuestions.length === generatedQuestions.length"
          >
            全部保存
          </Button>
        </div>
      </div>

      <div class="space-y-6">
        <Card
          v-for="(question, index) in generatedQuestions"
          :key="index"
          :class="{ 'border-green-200 bg-green-50': isQuestionSaved(question) }"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center">
              <span class="text-sm text-gray-500 mr-3">#{{ index + 1 }}</span>
              <h3 class="text-lg font-semibold text-gray-900">
                {{ question.title }}
              </h3>
            </div>
            <div class="flex items-center space-x-2">
              <span
                v-if="isQuestionSaved(question)"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
              >
                已保存
              </span>
              <DifficultyBadge :difficulty="question.difficulty" class="mr-2" />
              <CategoryBadge :category="question.category" />
            </div>
          </div>

          <div class="space-y-4">
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">题目描述</h4>
              <MarkdownRenderer :content="question.content" />
            </div>

            <div v-if="question.analysis">
              <h4 class="text-sm font-medium text-gray-700 mb-2">解题思路</h4>
              <MarkdownRenderer :content="question.analysis" />
            </div>

            <div v-if="question.tags.length > 0">
              <h4 class="text-sm font-medium text-gray-700 mb-2">标签</h4>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in question.tags"
                  :key="tag"
                  class="inline-block bg-gray-100 rounded px-3 py-1 text-sm"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <div class="flex justify-end pt-4 border-t border-gray-200">
              <Button
                v-if="!isQuestionSaved(question)"
                variant="primary"
                size="sm"
                @click="saveQuestion(question)"
                :loading="savingQuestion === question"
              >
                保存此题
              </Button>
              <Button
                v-else
                variant="secondary"
                size="sm"
                disabled
              >
                已保存
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">开始生成题目</h3>
      <p class="mt-1 text-sm text-gray-500">选择题目类别、难度和数量，然后点击生成题目</p>
    </div>

    <!-- 生成提示模态框 -->
    <Modal
      :show="showGenerateTip"
      title="AI生成说明"
      @update:show="showGenerateTip = $event"
    >
      <div class="text-gray-600">
        <p class="mb-4">
          题目生成功能使用OpenAI GPT模型，可能会产生以下情况：
        </p>
        <ul class="list-disc list-inside space-y-2 mb-4">
          <li>生成时间可能较长，请耐心等待</li>
          <li>生成的题目质量可能有差异，建议人工审核</li>
          <li>如果API密钥未配置，将使用模拟数据</li>
          <li>建议在生成后检查和编辑题目内容</li>
        </ul>
        <p>
          生成的题目可以直接保存到题库中，也可以重新生成。
        </p>
      </div>
      
      <template #footer>
        <Button variant="primary" @click="showGenerateTip = false">
          了解了
        </Button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useQuestionStore } from '@/stores'
import { categories, difficulties } from '@/types'
import type { Question } from '@/types'
import Card from '@/components/common/Card.vue'
import Button from '@/components/common/Button.vue'
import DifficultyBadge from '@/components/common/DifficultyBadge.vue'
import CategoryBadge from '@/components/common/CategoryBadge.vue'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'
import Modal from '@/components/common/Modal.vue'

const questionStore = useQuestionStore()

const generateParams = ref({
  category: '',
  difficulty: '',
  count: '' as any
})

const generatedQuestions = ref<Question[]>([])
const savedQuestions = ref<Question[]>([])
const generating = ref(false)
const saving = ref(false)
const savingQuestion = ref<Question | null>(null)
const showGenerateTip = ref(false)

const isFormValid = computed(() => {
  return generateParams.value.category &&
         generateParams.value.difficulty &&
         generateParams.value.count
})

onMounted(() => {
  showGenerateTip.value = true
})

const generateQuestions = async () => {
  if (!isFormValid.value) return
  
  generating.value = true
  try {
    const response = await questionStore.generateQuestions({
      category: generateParams.value.category,
      difficulty: generateParams.value.difficulty,
      count: generateParams.value.count
    })
    generatedQuestions.value = response
    savedQuestions.value = []
  } catch (error) {
    console.error('生成失败:', error)
  } finally {
    generating.value = false
  }
}

const regenerateQuestions = () => {
  generateQuestions()
}

const isQuestionSaved = (question: Question) => {
  return savedQuestions.value.some(saved => 
    saved.title === question.title && saved.content === question.content
  )
}

const saveQuestion = async (question: Question) => {
  savingQuestion.value = question
  try {
    const saved = await questionStore.createQuestion({
      title: question.title,
      content: question.content,
      category: question.category,
      difficulty: question.difficulty,
      analysis: question.analysis,
      tags: question.tags
    })
    savedQuestions.value.push(saved)
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    savingQuestion.value = null
  }
}

const saveAllQuestions = async () => {
  if (generatedQuestions.value.length === 0) return
  
  saving.value = true
  try {
    for (const question of generatedQuestions.value) {
      if (!isQuestionSaved(question)) {
        await saveQuestion(question)
      }
    }
  } catch (error) {
    console.error('批量保存失败:', error)
  } finally {
    saving.value = false
  }
}
</script>