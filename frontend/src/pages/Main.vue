<template>
  <div>
    <!-- 导航栏结构 -->
    <nav class="navbar">
      <div class="logo">音乐管理系统</div>
      <ul class="nav-links">
        <!-- 使用 @click 绑定点击事件，.prevent 阻止默认的 href 跳转 -->
        <li><div @click.prevent="currentTab = 'home'" :class="{ active: currentTab === 'home' }" class="nav-item">首页</div></li>
        <li><div @click.prevent="currentTab = 'artist'" :class="{ active: currentTab === 'artist' }" class="nav-item">歌手</div></li>
        <li><div @click.prevent="currentTab = 'album'" :class="{ active: currentTab === 'album' }" class="nav-item">专辑</div></li>
        <li><div @click.prevent="currentTab = 'song'" :class="{ active: currentTab === 'song' }" class="nav-item">歌曲</div></li>
        <li><div @click.prevent="currentTab = 'my'" :class="{ active: currentTab === 'my' }" class="nav-item">我的</div></li>
        <!-- 将退出按钮放入导航栏 -->
        <li><div @click="logout" class="logout-btn">退出登录</div></li>
      </ul>
    </nav>

    <div class="content">
      <!-- 根据 currentTab 的值显示不同的内容 -->
      <div v-if="currentTab === 'home'">
        <HomePage @play="playSong" />
      </div>

      <div v-else-if="currentTab === 'artist'">
        <ArtistList @select-artist="selectArtist" />
      </div>

      <div v-else-if="currentTab === 'artist_detail'">
        <ArtistDetail 
          :artist-id="currentArtistId" 
          @back="backToArtistList" 
          @play="playSong" 
          @select-album="selectAlbum"
        />
      </div>

      <div v-else-if="currentTab === 'album'">
        <AlbumList @select-album="selectAlbum" />
      </div>

      <div v-else-if="currentTab === 'album_detail'">
        <AlbumDetail 
          :album-id="currentAlbumId" 
          @back="backToAlbumList" 
          @play="playSong" 
        />
      </div>

      <div v-else-if="currentTab === 'song'">
        <SongList @play="playSong" />
      </div>

      <div v-else-if="currentTab === 'my'">
        <MinePage 
          @play="playSong" 
          @select-artist="selectArtist"
          @select-album="selectAlbum"
        />
      </div>
    </div>

    <!-- 全局播放器 -->
    <div v-if="currentSongUrl" class="audio-player-bar">
      <audio :src="currentSongUrl" controls autoplay></audio>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import HomePage from './subPages/Home.vue'
import MinePage from './subPages/MinePage.vue'
import ArtistList from './subPages/ArtistList.vue'
import AlbumList from './subPages/AlbumList.vue'
import SongList from './subPages/SongList.vue'
import ArtistDetail from './subPages/ArtistDetail.vue'
import AlbumDetail from './subPages/AlbumDetail.vue'

const user = ref(null)
const currentTab = ref('home') // 默认显示首页
const currentSongUrl = ref('')
const currentArtistId = ref(null)
const currentAlbumId = ref(null)

function playSong(url) {
  currentSongUrl.value = url
}

function selectArtist(id) {
  currentArtistId.value = id
  currentTab.value = 'artist_detail'
}

function selectAlbum(id) {
  currentAlbumId.value = id
  currentTab.value = 'album_detail'
}

function backToArtistList() {
  currentTab.value = 'artist'
  currentArtistId.value = null
}

function backToAlbumList() {
  currentTab.value = 'album'
  currentAlbumId.value = null
}

onMounted(() => {
  try {
    const userData = localStorage.getItem('user')
    if (userData) {
      user.value = JSON.parse(userData)
    }
  } catch (e) {}
})

function logout() {
  localStorage.removeItem('user')
  window.location.reload() // 刷新页面，App.vue 会重新检测并回到登录页
}
</script>

<style scoped>
/* 导航栏样式 */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333;
  color: white;
  padding: 1rem 2rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 20px;
  margin: 0;
  padding: 0;
  align-items: center;
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

/* 选中状态的样式 */
.nav-links .nav-item.active {
  background-color: #2563eb;
  /* 选中时变成蓝色背景 */
  color: white;
}

/* 页面内容样式 */
.content {
  padding: 40px;
  max-width: 1400px;
  margin: 0 auto; /* 内容居中 */
}

.logout-btn {
  padding: 6px 12px;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #d32f2f;
}

.dashboard-card, .data-placeholder {
  margin-top: 20px;
  padding: 20px;
  background: #f0f0f0;
  border-radius: 8px;
  border: 1px dashed #ccc;
}

.audio-player-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: #222;
  padding: 10px;
  display: flex;
  justify-content: center;
  z-index: 1000;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
}

audio {
  width: 80%;
  outline: none;
}
</style>