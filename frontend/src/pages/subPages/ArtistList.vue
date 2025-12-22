<template>
    <div class="artist-list-page">
        <h1>歌手列表</h1>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="artists.length === 0" class="empty">暂无歌手</div>
        <ul v-else class="artist-grid">
            <li v-for="artist in artists" :key="artist.id" class="artist-card" @click="$emit('select-artist', artist.id)">
                <div class="artist-info">
                    <h3>{{ artist.artist_name }}</h3>
                    <p class="region">地区: {{ artist.region || '未知' }}</p>
                    <p class="bio">{{ artist.bio || '暂无简介' }}</p>
                </div>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAllArtists } from '../../api/search'

const artists = ref([])
const loading = ref(true)
const error = ref(null)

const emit = defineEmits(['select-artist'])

onMounted(async () => {
    try {
        artists.value = await getAllArtists()
    } catch (e) {
        error.value = e.message || '加载歌手失败'
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.artist-list-page {
    padding: 20px;
}

.artist-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    list-style: none;
    padding: 0;
}

.artist-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    background: #fff;
    transition: transform 0.2s;
    cursor: pointer;
}

.artist-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.artist-info h3 {
    margin: 0 0 10px 0;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.region {
    color: #666;
    font-size: 0.9em;
    margin-bottom: 5px;
}

.bio {
    color: #888;
    font-size: 0.85em;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
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
