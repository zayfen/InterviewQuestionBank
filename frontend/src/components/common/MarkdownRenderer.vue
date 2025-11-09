<template>
  <div class="markdown-content" v-html="sanitizedHtml"></div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

interface Props {
  content: string
}

const props = defineProps<Props>()

const sanitizedHtml = computed(() => {
  const rawHtml = marked(props.content || '')
  return DOMPurify.sanitize(rawHtml)
})
</script>