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
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAllAlbums } from '../../api/search'

const albums = ref([])
const loading = ref(true)
const error = ref(null)

const emit = defineEmits(['select-album'])

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
    background: #fff;
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
}

.album-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.album-info h3 {
    margin: 0 0 10px 0;
    color: #333;
}

.release-time {
    color: #666;
    font-size: 0.9em;
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
