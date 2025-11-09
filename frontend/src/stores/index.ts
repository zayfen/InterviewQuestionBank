import { defineStore } from 'pinia'
import type { Question, QuestionListResponse } from '@/types'
import { questionApi, aiApi, randomApi, interviewApi } from '@/api'

export const useQuestionStore = defineStore('question', {
  state: () => ({
    questions: [] as Question[],
    currentQuestion: null as Question | null,
    total: 0,
    page: 1,
    size: 10,
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchQuestions(params?: { page?: number; size?: number; q?: string; category?: string; difficulty?: string }) {
      this.loading = true
      this.error = null
      try {
        const response = await questionApi.getQuestions(params)
        const data: QuestionListResponse = response.data
        this.questions = data.items
        this.total = data.total
        this.page = data.page
        this.size = data.size
      } catch (error: any) {
        this.error = error.message || '获取题目失败'
      } finally {
        this.loading = false
      }
    },

    async fetchQuestion(id: number) {
      this.loading = true
      this.error = null
      try {
        const response = await questionApi.getQuestion(id)
        this.currentQuestion = response.data
      } catch (error: any) {
        this.error = error.message || '获取题目详情失败'
      } finally {
        this.loading = false
      }
    },

    async createQuestion(question: any) {
      this.loading = true
      this.error = null
      try {
        const response = await questionApi.createQuestion(question)
        this.questions.unshift(response.data)
        this.total += 1
        return response.data
      } catch (error: any) {
        this.error = error.message || '创建题目失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateQuestion(id: number, question: any) {
      this.loading = true
      this.error = null
      try {
        const response = await questionApi.updateQuestion(id, question)
        const index = this.questions.findIndex(q => q.id === id)
        if (index !== -1) {
          this.questions[index] = response.data
        }
        return response.data
      } catch (error: any) {
        this.error = error.message || '更新题目失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteQuestion(id: number) {
      this.loading = true
      this.error = null
      try {
        await questionApi.deleteQuestion(id)
        this.questions = this.questions.filter(q => q.id !== id)
        this.total -= 1
      } catch (error: any) {
        this.error = error.message || '删除题目失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    setCurrentQuestion(question: Question | null) {
      this.currentQuestion = question
    },

    async generateQuestions(params: { category: string; difficulty: string; count: number }) {
      this.loading = true
      this.error = null
      try {
        const response = await aiApi.generateQuestions(params)
        return response.data
      } catch (error: any) {
        this.error = error.message || '生成题目失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getRandomQuestions(params: any) {
      this.loading = true
      this.error = null
      try {
        const response = await randomApi.getAdvancedRandomQuestions(params)
        return response.data.items
      } catch (error: any) {
        this.error = error.message || '获取随机题目失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    async getPresetInterview(presetType: string) {
      this.loading = true
      this.error = null
      try {
        const response = await interviewApi.getPresetInterview(presetType)
        return response.data
      } catch (error: any) {
        this.error = error.message || '获取预设面试失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    async createInterviewSession(config: any) {
      this.loading = true
      this.error = null
      try {
        const response = await interviewApi.createInterviewSession(config)
        return response.data
      } catch (error: any) {
        this.error = error.message || '创建面试会话失败'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})

export const useInterviewStore = defineStore('interview', {
  state: () => ({
    sessionQuestions: [] as Question[],
    currentIndex: 0,
    showAnalysis: false,
    sessionActive: false
  }),

  getters: {
    currentQuestion: (state) => {
      return state.sessionQuestions[state.currentIndex] || null
    },
    totalQuestions: (state) => state.sessionQuestions.length,
    progress: (state) => {
      if (state.sessionQuestions.length === 0) return 0
      return ((state.currentIndex + 1) / state.sessionQuestions.length) * 100
    }
  },

  actions: {
    startSession(questions: Question[]) {
      this.sessionQuestions = questions
      this.currentIndex = 0
      this.showAnalysis = false
      this.sessionActive = true
    },

    nextQuestion() {
      if (this.currentIndex < this.sessionQuestions.length - 1) {
        this.currentIndex += 1
        this.showAnalysis = false
      }
    },

    previousQuestion() {
      if (this.currentIndex > 0) {
        this.currentIndex -= 1
        this.showAnalysis = false
      }
    },

    toggleAnalysis() {
      this.showAnalysis = !this.showAnalysis
    },

    endSession() {
      this.sessionQuestions = []
      this.currentIndex = 0
      this.showAnalysis = false
      this.sessionActive = false
    }
  }
})