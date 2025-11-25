<template>
    <div class="mine-page">
        <h1>个人中心</h1>
        <nav class="mine-navbar">
            <ul class="nav-links">
                <li>
                    <div class="nav-item" @click="currentContent = 'favoriteSongsList'">收藏列表</div>
                </li>
                <li>
                    <div class="nav-item" @click="currentContent = 'favoriteAlbums'">专辑</div>
                </li>
                <li>
                    <div class="nav-item" @click="currentContent = 'favoriteArtists'">歌手</div>
                </li>
                <li>
                    <div class="nav-item" @click="currentContent = 'personalInfo'">个人信息</div>
                </li>
            </ul>
        </nav>
        <div v-if="currentContent != 'personalInfo'" class="favorites-section">
            <h2>我的收藏</h2>
            <div v-if="currentContent === 'favoriteSongsList'" class="fav-group">
                <div class="group-header">
                    <h3>收藏列表</h3>
                    <button class="add-list" @click="addList">添加收藏列表</button>
                </div>
                <div v-if="favoriteSongsList.length === 0" class="empty-tip">暂无收藏歌曲</div>
                <ul v-else class="fav-list">
                    <li v-for="song in favoriteSongsList" :key="song.id" class="fav-item">
                        <div class="fav-info">
                            <div class="fav-title">{{ song.title }}</div>
                        </div>
                        <button class="remove-btn" @click="removeList">💔</button>
                    </li>
                </ul>
            </div>
            <div v-if="currentContent === 'favoriteAlbums'" class="fav-group">
                <div class="group-header">
                    <h3>专辑</h3>
                </div>
                <div v-if="favoriteAlbums.length === 0" class="empty-tip">暂无收藏专辑</div>
                <ul v-else class="fav-list">
                    <li v-for="album in favoriteAlbums" :key="album.id" class="fav-item">
                        <div class="fav-info">
                            <div class="fav-title">{{ album.title }}</div>
                        </div>
                        <button class="remove-btn" @click="removeAlbum">💔</button>
                    </li>
                </ul>
            </div>
            <div v-if="currentContent === 'favoriteArtists'" class="fav-group">
                <div class="group-header">
                    <h3>歌手</h3>
                </div>
                <div v-if="favoriteArtists.length === 0" class="empty-tip">暂无关注歌手</div>
                <ul v-else class="fav-list">
                    <li v-for="artist in favoriteArtists" :key="artist.id" class="fav-item">
                        <div class="fav-info">
                            <div class="fav-title">{{ artist.title }}</div>
                        </div>
                        <button class="remove-btn" @click="removeArtist">💔</button>
                    </li>
                </ul>
            </div>
        </div>
        <div v-if="currentContent === 'personalInfo'" class="info-section">
            <h2>修改个人信息</h2>
            <div class="info-item">
                <span class="label">用户名</span>
                <input type="text" placeholder="请输入新的用户名" />
                <button>保存</button>
            </div>
            <div class="info-item">
                <span class="label">密码</span>
                <input type="text" placeholder="请输入新的密码" />
                <button>保存</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const currentContent = ref('favoriteSongsList')

// 模拟的收藏数据
const favoriteSongsList = ref([
    { id: 1, title: '收藏列表1' },
    { id: 2, title: '收藏列表2' },
    { id: 3, title: '收藏列表3' },
])

const favoriteAlbums = ref([
    { id: 1, title: '专辑1' },
    { id: 2, title: '专辑2' },
    { id: 3, title: '专辑3' },
])

const favoriteArtists = ref([
    { id: 1, title: '歌手1' },
    { id: 2, title: '歌手2' },
    { id: 3, title: '歌手3' },
])

function addList() {
    alert('添加收藏列表功能尚未实现')
}

function removeList() {
    alert('删除收藏列表功能尚未实现')
}

function removeAlbum() {
    alert('删除收藏专辑功能尚未实现')
}

function removeArtist() {
    alert('取消关注歌手功能尚未实现')
}
</script>

<style scoped>
.mine-page {
    padding: 24px;
    background: #fff;
    /* text-align: center;  <-- 去掉这个，让整体左对齐更自然 */
}

.mine-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #2a3d51; /* 深蓝灰色，比纯黑更有质感 */
    border-radius: 10px;
    color: white;
    padding: 1rem 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* 加一点阴影，增加立体感 */
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 20px;
    padding: 0;
    margin: 0;
}

.nav-links .nav-item {
    color: white;
    text-decoration: none;
    font-size: 1rem;
    padding: 5px 10px;
    border-radius: 4px;
    transition: background-color 0.3s;
    cursor: pointer;
}

.nav-links .nav-item:hover {
    color: #ddd;
    background-color: rgba(255, 255, 255, 0.1);
}

.favorites-section {
    margin-top: 20px;
    text-align: left;
    margin-left: 30px;
    max-width: 600px;
    /* 限制宽度，防止列表太宽 */
}

.fav-group h3 {
    font-size: 18px;
    color: #555;
    margin: 0;
    /* 去掉默认 margin，由父容器控制 */
}

.group-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    border-bottom: 2px solid #f0f0f0;
    padding-bottom: 10px;
}

.add-list {
    padding: 6px 14px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    /* 字体稍微改小一点，更协调 */
    cursor: pointer;
    transition: background-color 0.3s;
}

.add-list:hover {
    background-color: #45a049;
    /* 悬停加深 */
}

.fav-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.fav-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 15px;
    background: #f9f9f9;
    border-radius: 8px;
    margin-bottom: 10px;
    transition: transform 0.2s, box-shadow 0.2s;
}

.fav-item:hover {
    transform: translateY(-2px);
    /* 悬停微微上浮 */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    background: #fff;
}

.fav-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.fav-title {
    font-weight: bold;
    font-size: 16px;
    color: #333;
}

.remove-btn {
    background: none;
    border: none;
    font-size: 18px;
    cursor: pointer;
    padding: 8px;
    border-radius: 50%;
    transition: background-color 0.3s;
}

.remove-btn:hover {
    background-color: #ffebee;
    /* 悬停时显示浅红色背景 */
}

.empty-tip {
    color: #999;
    font-style: italic;
    padding: 20px 0;
}

.info-section {
    margin-top: 30px;
    text-align: left;
    margin-left: 30px;
}

.info-item {
    display: flex;
    align-items: center;
    /* 垂直居中对齐 */
    gap: 12px;
    max-width: 500px;
    /* 限制最大宽度，防止太长 */
    margin-top: 15px;
}

.label {
    font-weight: bold;
    color: #333;
    min-width: 60px;
    /* 给标签一个最小宽度，对齐更好看 */
}

.info-item input {
    flex: 1;
    /* 让输入框自动填满剩余空间 */
    padding: 8px 12px;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
}

.info-item input:focus {
    border-color: #2563eb;
    /* 聚焦时变蓝 */
}

.info-item button {
    padding: 6px 14px;
    background-color: #3cc0ef;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    /* 字体稍微改小一点，更协调 */
    cursor: pointer;
    transition: background-color 0.3s;
    white-space: nowrap;
    /* 防止按钮文字换行 */
}

.info-item button:hover {
    background-color: #3298eb;
    /* 悬停加深 */
}
</style>