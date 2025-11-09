export interface Question {
  id: number
  title: string
  content: string
  category: 'algorithm' | 'database' | 'system_design' | 'frontend' | 'backend' | 'devops' | 'mobile' | 'data_science' | 'security' | 'testing'
  difficulty: 'easy' | 'medium' | 'hard'
  analysis?: string
  tags: string[]
  created_at: string
  updated_at?: string
}

export interface QuestionListResponse {
  items: Question[]
  total: number
  page: number
  size: number
  pages: number
}

export interface QuestionCreate {
  title: string
  content: string
  category: Question['category']
  difficulty: Question['difficulty']
  analysis?: string
  tags: string[]
}

export interface QuestionUpdate {
  title?: string
  content?: string
  category?: Question['category']
  difficulty?: Question['difficulty']
  analysis?: string
  tags?: string[]
}

export interface QuestionSearchParams {
  q?: string
  category?: Question['category']
  difficulty?: Question['difficulty']
  page?: number
  size?: number
}

export interface QuestionGenerateRequest {
  category: Question['category']
  difficulty: Question['difficulty']
  count: number
}

export interface RandomQuestionRequest {
  count: number
  categories?: Question['category'][]
  difficulties?: Question['difficulty'][]
}

export interface InterviewSessionRequest {
  easy_count: number
  medium_count: number
  hard_count: number
}

export const categories = [
  { value: 'algorithm', label: '算法和数据结构' },
  { value: 'database', label: '数据库' },
  { value: 'system_design', label: '系统设计' },
  { value: 'frontend', label: '前端开发' },
  { value: 'backend', label: '后端开发' },
  { value: 'devops', label: '运维和DevOps' },
  { value: 'mobile', label: '移动开发' },
  { value: 'data_science', label: '数据科学' },
  { value: 'security', label: '网络安全' },
  { value: 'testing', label: '软件测试' }
] as const

export const difficulties = [
  { value: 'easy', label: '简单', color: 'green' },
  { value: 'medium', label: '中等', color: 'yellow' },
  { value: 'hard', label: '困难', color: 'red' }
] as const

export const categoryLabels: Record<Question['category'], string> = {
  algorithm: '算法和数据结构',
  database: '数据库',
  system_design: '系统设计',
  frontend: '前端开发',
  backend: '后端开发',
  devops: '运维和DevOps',
  mobile: '移动开发',
  data_science: '数据科学',
  security: '网络安全',
  testing: '软件测试'
}

export const difficultyLabels: Record<Question['difficulty'], string> = {
  easy: '简单',
  medium: '中等',
  hard: '困难'
}