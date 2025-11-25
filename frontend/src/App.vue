<template>
	<div id="app-root">
		<!-- 如果已登录（有 currentUser），显示主页 -->
		<MainPage v-if="currentUser" />

		<!-- 否则显示登录/注册页（使用居中布局） -->
		<div v-else class="login-layout">
			<LoginPage v-if="isLogin" />
			<RegisterPage v-else @switch-to-login="isLogin = true" />
			
			<div class="switch-btn" @click="isLogin = !isLogin">
				{{ isLogin ? '没有账号？去注册' : '已有账号？去登录' }}
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LoginPage from './pages/Login.vue'
import RegisterPage from './pages/Register.vue'
import MainPage from './pages/Main.vue'

const isLogin = ref(true)
const currentUser = ref(null)

// 页面加载时检查 localStorage
onMounted(() => {
	try {
		const savedUser = localStorage.getItem('user')
		if (savedUser) {
			currentUser.value = JSON.parse(savedUser)
		}
	} catch (e) {}
})
</script>

<style>
#app-root {
	min-height: 100vh;
	background: #f5f7fb;
}

/* 登录页面的专用居中布局 */
.login-layout {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	height: 100vh;
	width: 100%;
}

.switch-btn {
	margin-top: 16px;
	color: #2563eb;
	cursor: pointer;
	text-decoration: underline;
}
</style>