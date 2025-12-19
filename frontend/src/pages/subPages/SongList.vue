<template>
    <div class="song-list-page">
        <h1>歌曲列表</h1>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="songs.length === 0" class="empty">暂无歌曲</div>
        <ul v-else class="song-list">
            <li v-for="song in songs" :key="song.song_id" class="song-item">
                <div class="song-info">
                    <div class="song-title">{{ song.title }}</div>
                    <div class="song-meta">
                        <span>时长: {{ formatDuration(song.duration) }}</span>
                        <span>播放: {{ song.play_count }}</span>
                        <span>发行: {{ song.release_date }}</span>
                    </div>
                </div>
                <button class="play-btn" @click="emit('play', song.audio_url)">▶ 播放</button>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAllSongs } from '../../api/search'

const emit = defineEmits(['play'])
const songs = ref([])
const loading = ref(true)
const error = ref(null)

function formatDuration(seconds) {
    if (!seconds) return '0:00'
    const m = Math.floor(seconds / 60)
    const s = Math.floor(seconds % 60)
    return `${m}:${s.toString().padStart(2, '0')}`
}

onMounted(async () => {
    try {
        songs.value = await getAllSongs()
    } catch (e) {
        error.value = e.message || '加载歌曲失败'
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.song-list-page {
    padding: 20px;
}

.song-list {
    list-style: none;
    padding: 0;
}

.song-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #eee;
    background: #fff;
}

.song-item:hover {
    background-color: #f9f9f9;
}

.song-title {
    font-size: 1.1em;
    font-weight: bold;
    color: #333;
    margin-bottom: 5px;
}

.song-meta {
    font-size: 0.9em;
    color: #888;
}

.song-meta span {
    margin-right: 15px;
}

.play-btn {
    padding: 8px 16px;
    background-color: #1890ff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.play-btn:hover {
    background-color: #40a9ff;
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
