<template>
  <form class="login-form" @submit.prevent="submit">
    <div v-if="error" class="error">{{ error }}</div>
    <label>
      用户名 / 邮箱
      <input v-model="identifier" type="text" />
    </label>
    <label>
      密码
      <input v-model="password" type="password" />
    </label>
    <button type="submit" :disabled="loading">{{ loading ? '登录中...' : '登录' }}</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { login } from '../api/auth'

// 声明 emits（替代 Options API 中的 emits: []）
const emit = defineEmits(['success'])

const identifier = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

const submit = async () => {
  error.value = null
  if (!identifier.value || !password.value) {
    error.value = '请填写用户名和密码'
    return
  }
  loading.value = true
  try {
    const resp = await login({
      username: identifier.value,
      password: password.value
    })
    const tokens = resp?.data || resp
    emit('success', {
      username: identifier.value,
      access: tokens.access,
      refresh: tokens.refresh,
      role: tokens.role,
      userId: tokens.user_id
    })
  } catch (e) {
    error.value = e.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 12px
}

.login-form label {
  display: flex;
  flex-direction: column
}

.login-form input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px
}

.login-form .error {
  color: #b00020;
  background: #fff0f0;
  padding: 8px;
  border-radius: 6px
}

.login-form button {
  padding: 10px;
  border: 0;
  border-radius: 6px;
  background: #2563eb;
  color: #fff
}
</style>
