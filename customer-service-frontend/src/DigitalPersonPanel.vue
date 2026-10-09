<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'

const SDK_SRC = 'https://media.xingyun3d.com/xingyun3d/general/litesdk/xmovAvatar@latest.js'
const CREDENTIALS_ENDPOINT = '/api/digital-human/credentials'
// 后端凭证接口只下发 app_id/app_secret，gateway 与 avatar.html demo 保持一致
const GATEWAY_SERVER = 'https://nebula-agent.xingyun3d.com/user/v1/ttsa/session'

const status = ref('idle') // idle | connecting | ready
const progress = ref(0)

let sdk = null
let inited = false
let scriptPromise = null
let disposed = false // 连接中被取消时置 true，阻止 init 回调继续推进状态
const pendingTexts = []

const connectLabel = computed(() => {
  if (status.value === 'connecting') return '连接中…'
  if (status.value === 'ready') return '已连接'
  return '连接'
})

function loadSdkScript() {
  if (window.XmovAvatar) return Promise.resolve()
  if (scriptPromise) return scriptPromise
  scriptPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = SDK_SRC
    script.onload = resolve
    script.onerror = () => {
      scriptPromise = null
      reject(new Error('数字人 SDK 加载失败'))
    }
    document.head.appendChild(script)
  })
  return scriptPromise
}

async function fetchCredentials() {
  const response = await fetch(CREDENTIALS_ENDPOINT)
  const data = await response.json()
  if (!response.ok) {
    throw new Error(data.detail || '获取数字人凭证失败。')
  }
  if (!data.app_id || !data.app_secret) {
    throw new Error('数字人凭证不完整。')
  }
  return data
}

function flushPending() {
  if (!pendingTexts.length) return
  const text = pendingTexts.join('\n')
  pendingTexts.length = 0
  sdk.speak(text, true, true)
}

async function connect() {
  if (status.value !== 'idle') return
  status.value = 'connecting'
  progress.value = 0
  disposed = false
  try {
    const [credentials] = await Promise.all([fetchCredentials(), loadSdkScript()])
    if (disposed) return
    sdk = new window.XmovAvatar({
      containerId: '#digital-person-sdk',
      appId: credentials.app_id,
      appSecret: credentials.app_secret,
      gatewayServer: credentials.gateway_server || GATEWAY_SERVER,
      headers: {},
      hardwareAcceleration: 'prefer-hardware',
      enableLogger: false,
    })
    sdk.init({
      initModel: 'normal',
      onDownloadProgress(p) {
        if (disposed) return
        progress.value = p
        if (p >= 100 && !inited) {
          inited = true
          status.value = 'ready'
          flushPending()
        }
      },
    })
  } catch (error) {
    console.error('[digital-person]', error)
    if (!disposed) status.value = 'idle'
  }
}

// 取消连接 / 断开：销毁实例并复位（对应 avatar.html 的 doDestroy）
function disconnect() {
  if (status.value === 'idle') return
  disposed = true
  try { sdk?.destroy() } catch (e) { /* 忽略 */ }
  sdk = null
  inited = false
  pendingTexts.length = 0
  progress.value = 0
  status.value = 'idle'
}

// 对话响应到达时调用；未连接/未就绪期间暂存，就绪后补读
function speak(text) {
  if (!text) return
  if (inited && sdk) {
    sdk.speak(text, true, true)
  } else {
    pendingTexts.push(text)
  }
}

defineExpose({ speak })

onBeforeUnmount(() => {
  try { sdk?.destroy() } catch (e) { /* 忽略 */ }
})
</script>

<template>
  <aside class="dp-panel">
    <header class="dp-header">
      <h2>数字人</h2>
      <div class="dp-actions">
        <button
          type="button"
          class="dp-connect"
          :disabled="status !== 'idle'"
          @click="connect"
        >
          {{ connectLabel }}
        </button>
        <button
          v-if="status !== 'idle'"
          type="button"
          class="dp-cancel"
          @click="disconnect"
        >
          {{ status === 'connecting' ? '取消' : '断开' }}
        </button>
      </div>
    </header>

    <div class="dp-stage">
      <div id="digital-person-sdk"></div>
      <p v-if="status === 'idle'" class="dp-hint">点击「连接」初始化数字人</p>
      <p v-else-if="status === 'connecting'" class="dp-hint">资源下载中… {{ Math.round(progress) }}%</p>
    </div>

    <div v-if="status === 'connecting'" class="dp-progress">
      <div class="dp-progress-bar" :style="{ width: `${progress}%` }"></div>
    </div>
  </aside>
</template>

<style scoped>
.dp-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 48px);
  height: calc(100vh - 48px);
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(148, 163, 184, 0.28);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
}

.dp-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 20px 12px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}

.dp-header h2 {
  margin: 0;
  font-size: 18px;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.dp-actions {
  display: flex;
  gap: 8px;
}

.dp-connect {
  min-height: 36px;
  padding: 8px 16px;
  border: 1px solid rgba(148, 163, 184, 0.36);
  border-radius: 14px;
  background: linear-gradient(135deg, #1d4ed8, #2563eb);
  border-color: transparent;
  color: #eff6ff;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.2;
}

.dp-cancel {
  min-height: 36px;
  padding: 8px 16px;
  border: none;
  border-radius: 14px;
  background: #dc2626;
  color: #fff;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.2;
}

.dp-cancel:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 24px rgba(220, 38, 38, 0.22);
}

.dp-connect:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.22);
}

.dp-connect:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
  background: rgba(148, 163, 184, 0.45);
}

.dp-stage {
  position: relative;
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background: #ffffff;
}

.dp-stage :deep(#digital-person-sdk) {
  width: 100%;
  height: 100%;
  min-height: 0;
}

.dp-hint {
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  margin: 0;
  text-align: center;
  color: #61718a;
  font-size: 14px;
}

.dp-progress {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 4px;
  background: rgba(148, 163, 184, 0.3);
}

.dp-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #1d4ed8, #38bdf8);
  transition: width 0.3s;
}
</style>
