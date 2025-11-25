<template>
    <div class="home-page">
        <h1>欢迎来到音乐管理系统</h1>
        <p>在这里您可以管理您的音乐收藏，包括歌手、专辑和歌曲。</p>
        <div class="search">
            <input type="text" placeholder="搜索" v-model="query" />
            <button @click="search">搜索</button>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
const query = ref('')
function search() {
    alert(`搜索功能尚未实现，搜索关键词：${query.value}`)
}
</script>

<style scoped>
.home-page {
    padding: 24px;
    background: #fff;
    text-align: center;
}

.search {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    gap: 10px;
}

.search input {
    padding: 10px 15px;
    width: 300px;
    border: 2px solid #e0e0e0;
    border-radius: 25px; /* 圆角输入框 */
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
}

.search input:focus {
    border-color: #2563eb; /* 聚焦时变蓝 */
}

.search button {
    padding: 10px 24px;
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 25px; /* 圆角按钮 */
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.search button:hover {
    background-color: #1d4ed8; /* 悬停加深 */
}
</style>
