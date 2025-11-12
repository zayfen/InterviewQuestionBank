<template>
  <div class="markdown-content" v-html="sanitizedHtml"></div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

interface Props {
  content: string
}

const props = defineProps<Props>()

const renderer = new marked.Renderer();
renderer.code = function (code, language) {
  // Check if the language is a mermaid supported one
  if (language === 'mermaid' || code.match(/^sequenceDiagram/) || code.match(/^graph/)) {
    return '<pre class="mermaid">' + code + '</pre>';
  } else {
    return '<pre><code>' + code + '</code></pre>';
  }
};

// You can pass this renderer to your markdown parser
marked.setOptions({ renderer });

function deferRenderMermaid() {
  if (window.mermaid) {
    window.mermaid.run()
  }
}

const sanitizedHtml = computed(() => {
  const rawHtml = marked(props.content || '')
  return DOMPurify.sanitize(rawHtml)
})

onMounted(() => {
  deferRenderMermaid()
})
</script>
