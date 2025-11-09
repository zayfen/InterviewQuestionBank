import axios from 'axios'
import type { 
  Question, 
  QuestionListResponse, 
  QuestionCreate, 
  QuestionUpdate, 
  QuestionSearchParams,
  QuestionGenerateRequest,
  RandomQuestionRequest,
  InterviewSessionRequest
} from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 5 * 60 * 1000
})

export const questionApi = {
  // 获取题目列表
  getQuestions: (params?: QuestionSearchParams) => {
    return api.get<QuestionListResponse>('/questions', { params })
  },

  // 搜索题目
  searchQuestions: (params: QuestionSearchParams) => {
    return api.get<QuestionListResponse>('/questions/search', { params })
  },

  // 获取题目详情
  getQuestion: (id: number) => {
    return api.get<Question>(`/questions/${id}`)
  },

  // 创建题目
  createQuestion: (data: QuestionCreate) => {
    return api.post<Question>('/questions', data)
  },

  // 更新题目
  updateQuestion: (id: number, data: QuestionUpdate) => {
    return api.put<Question>(`/questions/${id}`, data)
  },

  // 删除题目
  deleteQuestion: (id: number) => {
    return api.delete<Question>(`/questions/${id}`)
  }
}

export const aiApi = {
  // AI生成题目
  generateQuestions: (data: QuestionGenerateRequest) => {
    return api.post<Question[]>('/ai/generate', data)
  },

  // 获取题目类别
  getCategories: () => {
    return api.get<string[]>('/ai/categories')
  },

  // 获取难度等级
  getDifficulties: () => {
    return api.get<string[]>('/ai/difficulties')
  }
}

export const randomApi = {
  // 随机获取题目
  getRandomQuestions: (params: { count: number; categories?: string[]; difficulties?: string[] }) => {
    return api.get<Question[]>('/random', { params })
  },

  // 高级随机选题
  getAdvancedRandomQuestions: (data: RandomQuestionRequest) => {
    return api.post<QuestionListResponse>('/random/advanced', data)
  }
}

export const interviewApi = {
  // 创建面试会话
  createInterviewSession: (data: InterviewSessionRequest) => {
    return api.post<QuestionListResponse>('/interview', data)
  },

  // 获取预设面试模式
  getPresetInterview: (presetType: string) => {
    return api.get<QuestionListResponse>(`/interview/preset/${presetType}`)
  }
}

export default api