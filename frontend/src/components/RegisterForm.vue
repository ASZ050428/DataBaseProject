<template>
    <form class="register-form" @submit.prevent="submit">
        <div v-if="error" class="error">{{ error }}</div>
        <label>
            用户名
            <input v-model="username" type="text" />
        </label>
        <label>
            邮箱
            <input v-model="email" type="email" />
        </label>
        <label>
            密码
            <input v-model="password" type="password" />
        </label>
        <button type="submit" :disabled="loading">{{ loading ? '注册中...' : '注册' }}</button>
    </form>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['success'])
const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

const submit = async () => {
    error.value = null
    if (!username.value || !email.value || !password.value) {
        error.value = '请填写所有字段'
        return
    }
    loading.value = true
    try {
        const user = {
            username: username.value,
            email: email.value,
            password: password.value
        }
        emit('success', user)
    } catch (e) {
        error.value = e.message || '注册失败'
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.register-form {
  display: flex;
  flex-direction: column;
  gap: 12px
}

.register-form label {
  display: flex;
  flex-direction: column
}

.register-form input {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 6px;
}

.register-form .error {
    color: #b00020;
    background: #fff0f0;
    padding: 8px;
    border-radius: 6px
}

.register-form button {
    padding: 10px;
    border: 0;
    border-radius: 6px;
    background: #44c408;
    color: #fff
}
</style>