import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/questions',
    name: 'Questions',
    component: () => import('@/views/QuestionsView.vue')
  },
  {
    path: '/questions/new',
    name: 'NewQuestion',
    component: () => import('@/views/QuestionFormView.vue')
  },
  {
    path: '/questions/:id/edit',
    name: 'EditQuestion',
    component: () => import('@/views/QuestionFormView.vue')
  },
  {
    path: '/generate',
    name: 'Generate',
    component: () => import('@/views/GenerateView.vue')
  },
  {
    path: '/random',
    name: 'Random',
    component: () => import('@/views/RandomView.vue')
  },
  {
    path: '/interview',
    name: 'Interview',
    component: () => import('@/views/InterviewView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router