<template>
    <div class="album-list-page">
        <h1>专辑列表</h1>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="albums.length === 0" class="empty">暂无专辑</div>
        <ul v-else class="album-grid">
            <li v-for="album in albums" :key="album.album_id" class="album-card" @click="$emit('select-album', album.album_id)">
                <div class="album-info">
                    <h3>{{ album.album_name }}</h3>
                    <p class="release-time">发行时间: {{ album.release_time }}</p>
                    <!-- 如果有歌手信息可以在这里显示，目前API只返回了 singer_id -->
                </div>
                <button class="action-btn btn-collect" @click.stop="handleCollectAlbum(album.album_id)">❤ 收藏</button>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAllAlbums } from '../../api/search'
import { addFavoriteAlbum } from '../../api/collection'
import { showMessage } from '../../utils/message'

const albums = ref([])
const loading = ref(true)
const error = ref(null)

const emit = defineEmits(['select-album'])

async function handleCollectAlbum(albumId) {
    try {
        await addFavoriteAlbum(albumId)
        showMessage('专辑收藏成功！', 'success')
    } catch (e) {
        showMessage(e.message || '收藏失败', 'error')
    }
}

onMounted(async () => {
    try {
        albums.value = await getAllAlbums()
    } catch (e) {
        error.value = e.message || '加载专辑失败'
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.album-list-page {
    padding: 20px;
}

.album-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    list-style: none;
    padding: 0;
}

.album-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    background: #fff;
    transition: transform 0.2s;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.album-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.album-info {
    margin-bottom: 15px;
}

.album-info h3 {
    margin: 0 0 10px 0;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.release-time {
    color: #666;
    font-size: 0.9em;
}

.action-btn {
    padding: 6px 16px;
    border: none;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    align-self: flex-start;
}

.btn-collect {
    background-color: #fff1f2;
    color: #e11d48;
}

.btn-collect:hover {
    background-color: #e11d48;
    color: white;
}

.loading, .error, .empty {
    text-align: center;
    padding: 40px;
    color: #666;
}

.error {
    color: #ff4d4f;
}
</style>
