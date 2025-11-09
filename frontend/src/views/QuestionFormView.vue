<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="sm:flex sm:items-center sm:justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">
          {{ isEdit ? '编辑题目' : '新建题目' }}
        </h1>
        <p class="mt-2 text-gray-600">
          {{ isEdit ? '更新现有题目的信息' : '创建一个新的面试题目' }}
        </p>
      </div>
      <div class="mt-4 sm:mt-0">
        <Button variant="secondary" @click="$router.push('/questions')">
          返回列表
        </Button>
      </div>
    </div>

    <Card>
      <form @submit.prevent="handleSubmit">
        <div class="space-y-6">
          <!-- 基本信息 -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                题目标题 *
              </label>
              <input
                v-model="form.title"
                type="text"
                class="input"
                placeholder="请输入题目标题"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                题目类别 *
              </label>
              <select v-model="form.category" class="select" required>
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
              <select v-model="form.difficulty" class="select" required>
                <option value="">请选择难度</option>
                <option v-for="difficulty in difficulties" :key="difficulty.value" :value="difficulty.value">
                  {{ difficulty.label }}
                </option>
              </select>
            </div>
          </div>

          <!-- 题目内容 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              题目内容 *
            </label>
            <textarea
              v-model="form.content"
              rows="8"
              class="textarea"
              placeholder="请输入题目详细描述，支持Markdown格式"
              required
            ></textarea>
            <p class="mt-1 text-sm text-gray-500">
              支持Markdown格式，可以使用 **粗体**、*斜体*、列表等格式
            </p>
          </div>

          <!-- 解题思路 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              解题思路和分析
            </label>
            <textarea
              v-model="form.analysis"
              rows="6"
              class="textarea"
              placeholder="请输入解题思路、关键点和详细分析"
            ></textarea>
            <p class="mt-1 text-sm text-gray-500">
              提供详细的解题步骤和思路，帮助面试者理解问题
            </p>
          </div>

          <!-- 标签 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              标签
            </label>
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="tag in form.tags"
                :key="tag"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-gray-100 text-gray-800"
              >
                {{ tag }}
                <button
                  type="button"
                  class="ml-2 text-gray-500 hover:text-gray-700"
                  @click="removeTag(tag)"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </span>
            </div>
            <div class="flex">
              <input
                v-model="newTag"
                type="text"
                class="input flex-1 mr-2"
                placeholder="输入标签后按回车添加"
                @keyup.enter="addTag"
              />
              <Button variant="secondary" @click="addTag">
                添加
              </Button>
            </div>
          </div>

          <!-- 预览 -->
          <div v-if="form.content">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              题目预览
            </label>
            <div class="bg-gray-50 rounded-lg p-4">
              <MarkdownRenderer :content="form.content" />
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
          <Button variant="secondary" @click="$router.push('/questions')">
            取消
          </Button>
          <Button
            variant="primary"
            type="submit"
            :loading="saving"
            :disabled="!isFormValid"
          >
            {{ isEdit ? '更新题目' : '创建题目' }}
          </Button>
        </div>
      </form>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuestionStore } from '@/stores'
import { categories, difficulties } from '@/types'
import type { QuestionCreate, QuestionUpdate } from '@/types'
import Card from '@/components/common/Card.vue'
import Button from '@/components/common/Button.vue'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'

const route = useRoute()
const router = useRouter()
const questionStore = useQuestionStore()

const isEdit = computed(() => !!route.params.id)
const saving = ref(false)
const newTag = ref('')

const form = ref<QuestionCreate>({
  title: '',
  content: '',
  category: '',
  difficulty: '',
  analysis: '',
  tags: []
})

const isFormValid = computed(() => {
  return form.value.title.trim() &&
         form.value.content.trim() &&
         form.value.category &&
         form.value.difficulty
})

onMounted(async () => {
  if (isEdit.value) {
    const id = Number(route.params.id)
    await questionStore.fetchQuestion(id)
    if (questionStore.currentQuestion) {
      form.value = {
        title: questionStore.currentQuestion.title,
        content: questionStore.currentQuestion.content,
        category: questionStore.currentQuestion.category,
        difficulty: questionStore.currentQuestion.difficulty,
        analysis: questionStore.currentQuestion.analysis || '',
        tags: [...questionStore.currentQuestion.tags]
      }
    }
  }
})

const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !form.value.tags.includes(tag)) {
    form.value.tags.push(tag)
    newTag.value = ''
  }
}

const removeTag = (tag: string) => {
  const index = form.value.tags.indexOf(tag)
  if (index > -1) {
    form.value.tags.splice(index, 1)
  }
}

const handleSubmit = async () => {
  if (!isFormValid.value) return
  
  saving.value = true
  try {
    if (isEdit.value) {
      const id = Number(route.params.id)
      const updateData: QuestionUpdate = {
        title: form.value.title,
        content: form.value.content,
        category: form.value.category as any,
        difficulty: form.value.difficulty as any,
        analysis: form.value.analysis,
        tags: form.value.tags
      }
      await questionStore.updateQuestion(id, updateData)
    } else {
      await questionStore.createQuestion(form.value)
    }
    router.push('/questions')
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    saving.value = false
  }
}
</script>