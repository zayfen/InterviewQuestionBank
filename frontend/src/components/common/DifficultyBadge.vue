<template>
  <span :class="badgeClass">
    {{ label }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Question } from '@/types'
import { difficultyLabels } from '@/types'

interface Props {
  difficulty: Question['difficulty']
}

const props = defineProps<Props>()

const label = computed(() => difficultyLabels[props.difficulty])

const badgeClass = computed(() => {
  const baseClasses = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium'
  
  const difficultyClasses = {
    easy: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    hard: 'bg-red-100 text-red-800'
  }
  
  return `${baseClasses} ${difficultyClasses[props.difficulty]}`
})
</script>