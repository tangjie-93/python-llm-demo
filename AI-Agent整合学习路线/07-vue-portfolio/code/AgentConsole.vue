<script setup lang="ts">
import { computed, ref } from 'vue'

type ToolCall = {
  id: string
  name: string
  status: 'pending' | 'approved' | 'done' | 'failed'
  summary: string
}

type Message = {
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
}

const input = ref('')
const running = ref(false)
const messages = ref<Message[]>([
  { role: 'assistant', content: '你好，我可以帮你查询知识库并执行经过审批的业务操作。' },
])
const toolCalls = ref<ToolCall[]>([])

const canSend = computed(() => input.value.trim().length > 0 && !running.value)

function sendMessage() {
  if (!canSend.value) return
  const content = input.value.trim()
  messages.value.push({ role: 'user', content })
  input.value = ''
  running.value = true

  const toolCall: ToolCall = {
    id: crypto.randomUUID(),
    name: 'search_docs',
    status: 'done',
    summary: `检索与“${content}”相关的资料`,
  }
  toolCalls.value.unshift(toolCall)
  messages.value.push({
    role: 'assistant',
    content: '已根据知识库生成回答。高风险操作会先进入审批队列。',
    sources: ['docs/rag.md', 'docs/tool-calling.md'],
  })
  running.value = false
}

function approveTool(id: string) {
  const tool = toolCalls.value.find((item) => item.id === id)
  if (tool) tool.status = 'approved'
}
</script>

<template>
  <main class="agent-console">
    <section class="messages">
      <article v-for="(message, index) in messages" :key="index" :class="message.role">
        <p>{{ message.content }}</p>
        <small v-if="message.sources?.length">来源：{{ message.sources.join(', ') }}</small>
      </article>
    </section>

    <aside class="tools">
      <h2>工具调用</h2>
      <article v-for="tool in toolCalls" :key="tool.id">
        <strong>{{ tool.name }}</strong>
        <p>{{ tool.summary }}</p>
        <button v-if="tool.status === 'pending'" type="button" @click="approveTool(tool.id)">
          审批
        </button>
        <span>{{ tool.status }}</span>
      </article>
    </aside>

    <form class="composer" @submit.prevent="sendMessage">
      <input v-model="input" placeholder="输入任务或问题" />
      <button type="submit" :disabled="!canSend">发送</button>
    </form>
  </main>
</template>

<style scoped>
.agent-console {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 16px;
  min-height: 640px;
}

.messages,
.tools {
  border: 1px solid #d6dde8;
  border-radius: 8px;
  padding: 16px;
}

article {
  margin-bottom: 12px;
}

.user {
  text-align: right;
}

.composer {
  grid-column: 1 / -1;
  display: flex;
  gap: 8px;
}

input {
  flex: 1;
  padding: 10px 12px;
}

button {
  padding: 10px 14px;
}
</style>

