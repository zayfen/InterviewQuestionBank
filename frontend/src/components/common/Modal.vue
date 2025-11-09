<template>
  <Teleport to="body">
    <Transition
      enter-active-class="ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="show"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="handleBackdropClick"
      >
        <!-- Background overlay -->
        <div class="absolute inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

        <!-- Modal panel -->
        <Transition
          enter-active-class="ease-out duration-300"
          enter-from-class="opacity-0 translate-y-4 scale-95"
          enter-to-class="opacity-100 translate-y-0 scale-100"
          leave-active-class="ease-in duration-200"
          leave-from-class="opacity-100 translate-y-0 scale-100"
          leave-to-class="opacity-0 translate-y-4 scale-95"
        >
          <div
            v-if="show"
            class="relative bg-white rounded-lg shadow-xl transform transition-all w-full"
            :class="[sizeClass, heightClass]"
            @click.stop
          >
            <!-- Header with close button -->
            <div class="flex items-start justify-between px-6 py-4 border-b border-gray-200">
              <h3 v-if="title" class="text-lg font-semibold text-gray-900">
                {{ title }}
              </h3>
              <button
                v-if="showClose"
                @click="emit('update:show', false)"
                class="ml-4 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-md"
                type="button"
              >
                <span class="sr-only">关闭</span>
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <!-- Scrollable content area -->
            <div class="px-6 py-4 overflow-y-auto" :class="contentHeightClass">
              <slot></slot>
            </div>
            
            <!-- Footer -->
            <div v-if="$slots.footer" class="flex flex-row-reverse gap-3 px-6 py-4 bg-gray-50 border-t border-gray-200">
              <slot name="footer"></slot>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  show: boolean
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl'
  fixedHeight?: boolean
  closeOnBackdrop?: boolean
  showClose?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  fixedHeight: false,
  closeOnBackdrop: true,
  showClose: true
})

const emit = defineEmits<{
  'update:show': [show: boolean]
}>()

const sizeClass = computed(() => {
  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-2xl',
    xl: 'max-w-3xl',
    '2xl': 'max-w-4xl',
    '3xl': 'max-w-5xl',
    '4xl': 'max-w-6xl'
  }
  return sizeClasses[props.size]
})

const heightClass = computed(() => {
  return props.fixedHeight ? 'max-h-[80vh] flex flex-col' : 'max-h-[90vh]'
})

const contentHeightClass = computed(() => {
  return props.fixedHeight ? 'flex-1' : 'max-h-[calc(90vh-180px)]'
})

const handleBackdropClick = () => {
  if (props.closeOnBackdrop) {
    emit('update:show', false)
  }
}
</script>