<template>
    <div class="page-register">
        <h2>注册</h2>
        <RegisterForm @success="onSuccess" />
    </div>
</template>

<script setup>
import RegisterForm from '../components/RegisterForm.vue'

// 定义事件，通知父组件切换
const emit = defineEmits(['switchToLogin'])

function onSuccess(user) {
    try {
        localStorage.setItem('user', JSON.stringify(user)) 
    } catch (e) {
        console.error('Failed to save user to localStorage', e)
    }
    // 注册成功后，通知父组件切换到登录页
    emit('switchToLogin')
}
</script>

<style scoped>
.page-register {
    width: 100%;
    max-width: 420px;
    padding: 24px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 6px 18px rgba(10, 10, 20, 0.08)
}
</style>