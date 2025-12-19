<template>
    <div class="album-detail-page">
        <button class="back-btn" @click="$emit('back')">← 返回列表</button>
        
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else class="content">
            <div class="header">
                <h1>{{ album.album_name }}</h1>
                <p class="meta">发行时间: {{ album.release_time }}</p>
            </div>

            <div class="section">
                <h2>歌曲列表</h2>
                <div v-if="!album.songs || album.songs.length === 0" class="empty">该专辑暂无歌曲</div>
                <ul v-else class="song-list">
                    <li v-for="song in album.songs" :key="song.song_id" class="song-item">
                        <span class="index">{{ song.song_id }}</span> <!-- 也可以用 index + 1 -->
                        <span class="song-title">{{ song.title }}</span>
                        <div class="actions">
                            <span class="duration">{{ formatDuration(song.duration) }}</span>
                            <button class="play-btn" @click="$emit('play', song.audio_url)">▶</button>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { getAlbumDetail } from '../../api/search'

const props = defineProps({
    albumId: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['back', 'play'])

const album = ref({})
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
        album.value = await getAlbumDetail(props.albumId)
    } catch (e) {
        error.value = e.message || '加载详情失败'
    } finally {
        loading.value = false
    }
}

onMounted(loadData)
watch(() => props.albumId, loadData)
</script>

<style scoped>
.album-detail-page {
    padding: 20px;
}

.back-btn {
    margin-bottom: 20px;
    padding: 8px 16px;
    background: #f0f0f0;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.header {
    margin-bottom: 30px;
    border-bottom: 1px solid #eee;
    padding-bottom: 20px;
}

.meta {
    color: #666;
    margin-top: 10px;
}

.song-list {
    list-style: none;
    padding: 0;
}

.song-item {
    display: flex;
    align-items: center;
    padding: 12px;
    border-bottom: 1px solid #eee;
}

.song-item:hover {
    background-color: #f9f9f9;
}

.index {
    width: 40px;
    color: #999;
}

.song-title {
    flex: 1;
    font-weight: 500;
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

.loading, .error, .empty {
    text-align: center;
    color: #666;
    padding: 20px;
}

.error {
    color: #ff4d4f;
}
</style>
