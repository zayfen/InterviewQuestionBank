<template>
  <span class="badge bg-blue-100 text-blue-800">
    {{ label }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Question } from '@/types'
import { categoryLabels } from '@/types'

interface Props {
  category: Question['category']
}

const props = defineProps<Props>()

const label = computed(() => categoryLabels[props.category])
</script>