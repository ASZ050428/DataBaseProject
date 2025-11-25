<template>
  <div class="page-login">
    <h2>登录</h2>
    <LoginForm @success="onSuccess" />
  </div>
</template>

<script setup>
import LoginForm from '../components/LoginForm.vue'

function onSuccess(user) {
  try {
    localStorage.setItem('user', JSON.stringify(user)) 
    // 登录成功后，直接刷新页面，App.vue 会读取 localStorage 并显示主页
    window.location.reload()
  } catch (e) {
    console.error('Failed to save user to localStorage', e)
  }
}
</script>

<style scoped>
.page-login {
  width: 100%;
  max-width: 420px;
  padding: 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 6px 18px rgba(10, 10, 20, 0.08)
}

.page-login h2 {
  margin: 0 0 12px
}
</style>
