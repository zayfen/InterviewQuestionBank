<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="sm:flex sm:items-center sm:justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">题目管理</h1>
        <p class="mt-2 text-gray-600">管理您的面试题库，支持搜索、筛选和编辑</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <Button variant="primary" @click="$router.push('/questions/new')">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          新建题目
        </Button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <Card class="mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">搜索</label>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索题目标题或内容..."
            class="input"
            @keyup.enter="handleSearch"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">类别</label>
          <select v-model="selectedCategory" class="select">
            <option value="">全部类别</option>
            <option v-for="category in categories" :key="category.value" :value="category.value">
              {{ category.label }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">难度</label>
          <select v-model="selectedDifficulty" class="select">
            <option value="">全部难度</option>
            <option v-for="difficulty in difficulties" :key="difficulty.value" :value="difficulty.value">
              {{ difficulty.label }}
            </option>
          </select>
        </div>
        <div class="flex items-end">
          <Button variant="secondary" @click="handleSearch" class="mr-2">
            搜索
          </Button>
          <Button variant="secondary" @click="resetFilters">
            重置
          </Button>
        </div>
      </div>
    </Card>

    <!-- 题目列表 -->
    <Loading v-if="questionStore.loading" text="加载题目中..." />
    
    <div v-else-if="questionStore.questions.length > 0" class="space-y-4">
      <Card
        v-for="question in questionStore.questions"
        :key="question.id"
        class="hover:shadow-md transition-shadow"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center mb-2">
              <h3 class="text-lg font-semibold text-gray-900 mr-3">
                {{ question.title }}
              </h3>
              <DifficultyBadge :difficulty="question.difficulty" class="mr-2" />
              <CategoryBadge :category="question.category" />
            </div>
            <p class="text-gray-600 mb-3 line-clamp-2">
              {{ question.content }}
            </p>
            <div class="flex items-center text-sm text-gray-500">
              <span>创建时间: {{ formatDate(question.created_at) }}</span>
              <span v-if="question.tags.length > 0" class="ml-4">
                标签: 
                <span v-for="tag in question.tags" :key="tag" class="inline-block bg-gray-100 rounded px-2 py-1 text-xs mr-1">
                  {{ tag }}
                </span>
              </span>
            </div>
          </div>
          <div class="flex items-center space-x-2 ml-4">
            <Button
              variant="secondary"
              size="sm"
              @click="viewQuestion(question)"
            >
              查看
            </Button>
            <Button
              variant="secondary"
              size="sm"
              @click="editQuestion(question)"
            >
              编辑
            </Button>
            <Button
              variant="danger"
              size="sm"
              @click="confirmDelete(question)"
            >
              删除
            </Button>
          </div>
        </div>
      </Card>

      <!-- 分页 -->
      <div class="flex items-center justify-between mt-8">
        <div class="text-sm text-gray-700">
          共 {{ questionStore.total }} 条记录
        </div>
        <div class="flex space-x-2">
          <Button
            variant="secondary"
            size="sm"
            :disabled="questionStore.page <= 1"
            @click="changePage(questionStore.page - 1)"
          >
            上一页
          </Button>
          <span class="inline-flex items-center px-4 py-2 text-sm text-gray-700">
            第 {{ questionStore.page }} 页
          </span>
          <Button
            variant="secondary"
            size="sm"
            :disabled="questionStore.page >= Math.ceil(questionStore.total / questionStore.size)"
            @click="changePage(questionStore.page + 1)"
          >
            下一页
          </Button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">暂无题目</h3>
      <p class="mt-1 text-sm text-gray-500">开始创建您的第一个面试题目吧</p>
      <div class="mt-6">
        <Button variant="primary" @click="$router.push('/questions/new')">
          新建题目
        </Button>
      </div>
    </div>

    <!-- 题目详情模态框 -->
    <Modal
      :show="showDetailModal"
      :title="currentQuestion?.title"
      size="3xl"
      :fixed-height="true"
      @update:show="showDetailModal = $event"
    >
      <div v-if="currentQuestion">
        <div class="mb-4">
          <div class="flex items-center mb-3">
            <DifficultyBadge :difficulty="currentQuestion.difficulty" class="mr-2" />
            <CategoryBadge :category="currentQuestion.category" />
          </div>
        </div>
        
        <div class="mb-6">
          <h4 class="text-lg font-medium text-gray-900 mb-2">题目描述</h4>
          <MarkdownRenderer :content="currentQuestion.content" />
        </div>
        
        <div v-if="currentQuestion.analysis" class="mb-6">
          <h4 class="text-lg font-medium text-gray-900 mb-2">解题思路</h4>
          <MarkdownRenderer :content="currentQuestion.analysis" />
        </div>
        
        <div v-if="currentQuestion.tags.length > 0" class="mb-6">
          <h4 class="text-lg font-medium text-gray-900 mb-2">标签</h4>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="tag in currentQuestion.tags"
              :key="tag"
              class="inline-block bg-gray-100 rounded px-3 py-1 text-sm"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
      
      <template #footer>
        <Button variant="primary" @click="editQuestion(currentQuestion!)">
          编辑
        </Button>
        <Button variant="secondary" @click="showDetailModal = false">
          关闭
        </Button>
      </template>
    </Modal>

    <!-- 删除确认模态框 -->
    <Modal
      :show="showDeleteModal"
      title="确认删除"
      @update:show="showDeleteModal = $event"
    >
      <p class="text-gray-600">
        确定要删除题目 "{{ questionToDelete?.title }}" 吗？此操作无法撤销。
      </p>
      
      <template #footer>
        <Button variant="secondary" @click="showDeleteModal = false">
          取消
        </Button>
        <Button variant="danger" @click="deleteQuestion" :loading="deleting">
          删除
        </Button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuestionStore } from '@/stores'
import { categories, difficulties } from '@/types'
import type { Question } from '@/types'
import Card from '@/components/common/Card.vue'
import Button from '@/components/common/Button.vue'
import Loading from '@/components/common/Loading.vue'
import Modal from '@/components/common/Modal.vue'
import DifficultyBadge from '@/components/common/DifficultyBadge.vue'
import CategoryBadge from '@/components/common/CategoryBadge.vue'
import MarkdownRenderer from '@/components/common/MarkdownRenderer.vue'

const router = useRouter()
const questionStore = useQuestionStore()

const searchQuery = ref('')
const selectedCategory = ref('')
const selectedDifficulty = ref('')
const showDetailModal = ref(false)
const showDeleteModal = ref(false)
const currentQuestion = ref<Question | null>(null)
const questionToDelete = ref<Question | null>(null)
const deleting = ref(false)

onMounted(() => {
  questionStore.fetchQuestions()
})

const handleSearch = () => {
  questionStore.fetchQuestions({
    q: searchQuery.value || undefined,
    category: selectedCategory.value || undefined,
    difficulty: selectedDifficulty.value || undefined,
    page: 1
  })
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  selectedDifficulty.value = ''
  handleSearch()
}

const changePage = (newPage: number) => {
  questionStore.fetchQuestions({
    page: newPage,
    q: searchQuery.value || undefined,
    category: selectedCategory.value || undefined,
    difficulty: selectedDifficulty.value || undefined
  })
}

const viewQuestion = (question: Question) => {
  currentQuestion.value = question
  showDetailModal.value = true
}

const editQuestion = (question: Question) => {
  router.push(`/questions/${question.id}/edit`)
}

const confirmDelete = (question: Question) => {
  questionToDelete.value = question
  showDeleteModal.value = true
}

const deleteQuestion = async () => {
  if (!questionToDelete.value) return
  
  deleting.value = true
  try {
    await questionStore.deleteQuestion(questionToDelete.value.id)
    showDeleteModal.value = false
    questionToDelete.value = null
  } catch (error) {
    console.error('删除失败:', error)
  } finally {
    deleting.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}
</script>