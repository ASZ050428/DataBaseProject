<template>
    <div class="artist-detail-page">
        <button class="back-btn" @click="$emit('back')">返回列表</button>

        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else class="content">
            <div class="header">
                <h1>{{ artist.artist_name }}</h1>
                <p class="region">地区: {{ artist.region || '未知' }}</p>
                <p class="bio">{{ artist.bio || '暂无简介' }}</p>
            </div>

            <div class="section">
                <h2>热门歌曲</h2>
                <div v-if="!artist.songs || artist.songs.length === 0" class="empty">暂无歌曲</div>
                <ul v-else class="song-list">
                    <li v-for="song in artist.songs" :key="song.song_id" class="song-item">
                        <span class="song-title">{{ song.title }}</span>
                        <div class="actions">
                            <span class="duration">{{ formatDuration(song.duration) }}</span>
                            <button class="play-btn" @click="$emit('play', song.audio_url)">▶</button>
                        </div>
                    </li>
                </ul>
            </div>

            <div class="section">
                <h2>专辑</h2>
                <div v-if="!artist.albums || artist.albums.length === 0" class="empty">暂无专辑</div>
                <ul v-else class="album-grid">
                    <li v-for="album in artist.albums" :key="album.album_id" class="album-card"
                        @click="$emit('select-album', album.album_id)">
                        <div class="album-info">
                            <h3>{{ album.album_name }}</h3>
                            <p class="release-time">{{ album.release_time }}</p>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { getArtistDetail } from '../../api/search'

const props = defineProps({
    artistId: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['back', 'play', 'select-album'])

const artist = ref({})
const loading = ref(true)
const error = ref(null)

function formatDuration(seconds) {
    if (!seconds) return '0:00'
    const m = Math.floor(seconds / 60)
    const s = Math.floor(seconds % 60)
    return `${m}:${s.toString().padStart(2, '0')}`
}

async function loadData() {
    loading.value = true
    error.value = null
    try {
        artist.value = await getArtistDetail(props.artistId)
    } catch (e) {
        error.value = e.message || '加载详情失败'
    } finally {
        loading.value = false
    }
}

onMounted(loadData)
watch(() => props.artistId, loadData)
</script>

<style scoped>
.artist-detail-page {
    padding: 20px;
}

.back-btn {
    padding: 6px 12px;
    background-color: #ed3a3a;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    color: white;
    transition: all 0.3s;
}

.back-btn:hover {
    background-color: #b11a1a;
}

.header {
    margin-bottom: 30px;
    border-bottom: 1px solid #eee;
    padding-bottom: 20px;
}

.bio {
    color: #666;
    line-height: 1.6;
    margin-top: 10px;
}

.section {
    margin-bottom: 40px;
}

.song-list {
    list-style: none;
    padding: 0;
}

.song-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #eee;
}

.song-item:hover {
    background-color: #f9f9f9;
}

.actions {
    display: flex;
    align-items: center;
    gap: 15px;
}

.play-btn {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: none;
    background: #1890ff;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.album-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 20px;
    list-style: none;
    padding: 0;
}

.album-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    cursor: pointer;
    transition: transform 0.2s;
}

.album-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.album-info h3 {
    margin: 0 0 5px 0;
    font-size: 1rem;
}

.loading,
.error,
.empty {
    text-align: center;
    color: #666;
    padding: 20px;
}

.error {
    color: #ff4d4f;
}
</style>
