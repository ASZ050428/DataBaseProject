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
                <button class="action-btn btn-follow" @click.stop="handleFollowArtist(artist.artist_id || artist.id)">＋ 关注</button>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAllArtists } from '../../api/search'
import { addFavoriteArtist } from '../../api/collection'
import { showMessage } from '../../utils/message'

const artists = ref([])
const loading = ref(true)
const error = ref(null)

const emit = defineEmits(['select-artist'])

async function handleFollowArtist(artistId) {
    try {
        await addFavoriteArtist(artistId)
        showMessage('关注成功', 'success')
    } catch (e) {
        showMessage(e.message || '关注失败', 'error')
    }
}

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
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.artist-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.artist-info {
    margin-bottom: 15px;
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

.btn-follow {
    background-color: #f0fdf4;
    color: #16a34a;
}

.btn-follow:hover {
    background-color: #16a34a;
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
