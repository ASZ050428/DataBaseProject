<template>
    <div class="mine-page">
        <h1>个人中心</h1>
        <nav class="mine-navbar">
            <ul class="nav-links">
                <li>
                    <div class="nav-item" @click="currentContent = 'FavoriteSongs'">收藏列表</div>
                </li>
                <li>
                    <div class="nav-item" @click="currentContent = 'FavoriteAlbums'">专辑</div>
                </li>
                <li>
                    <div class="nav-item" @click="currentContent = 'FavoriteArtists'">歌手</div>
                </li>
                <li>
                    <div class="nav-item" @click="currentContent = 'PersonalInfo'">个人信息</div>
                </li>
                <li v-if="isArtist">
                    <div class="nav-item" @click="currentContent = 'CreatorCenter'">创作者中心</div>
                </li>
            </ul>
        </nav>

        <div class="content-area">
            <component 
                :is="components[currentContent]" 
                @play="(url) => emit('play', url)"
                @select-album="(id) => emit('select-album', id)"
                @select-artist="(id) => emit('select-artist', id)"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUserInfo } from '../../api/user'

// Import Sub-components
import FavoriteSongs from './MinePageSubPages/FavoriteSongs.vue'
import FavoriteAlbums from './MinePageSubPages/FavoriteAlbums.vue'
import FavoriteArtists from './MinePageSubPages/FavoriteArtists.vue'
import PersonalInfo from './MinePageSubPages/PersonalInfo.vue'
import CreatorCenter from './MinePageSubPages/CreatorCenter.vue'

const emit = defineEmits(['play', 'select-album', 'select-artist'])

const currentContent = ref('FavoriteSongs')
const isArtist = ref(false)

const components = {
    FavoriteSongs,
    FavoriteAlbums,
    FavoriteArtists,
    PersonalInfo,
    CreatorCenter
}

onMounted(async () => {
    await checkUserRole()
})

async function checkUserRole() {
    try {
        const userStr = localStorage.getItem('user')
        if (userStr) {
            const user = JSON.parse(userStr)
            isArtist.value = user.role === 'artist'
        }
        
        // Fetch latest info to be sure
        const userInfo = await getUserInfo()
        if (userInfo) {
            isArtist.value = userInfo.role === 'artist'
            
            // Update local storage
            const localUser = JSON.parse(localStorage.getItem('user') || '{}')
            localUser.role = userInfo.role
            localUser.artist_id = userInfo.artist_id
            localStorage.setItem('user', JSON.stringify(localUser))
        }
    } catch (e) {
        console.warn('获取用户信息失败', e)
    }
}
</script>

<style scoped>
.mine-page {
    padding: 24px;
    background: #fff;
}

.mine-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #2a3d51;
    border-radius: 10px;
    color: white;
    padding: 1rem 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 20px;
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

.content-area {
    margin-top: 20px;
    padding: 0 20px;
}
</style>