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
                <div class="actions">
                    <button class="action-btn btn-play" @click="emit('play', song.audio_url)">▶ 播放</button>
                    <button class="action-btn btn-collect" @click="openCollectModal(song.song_id)">❤ 收藏</button>
                </div>
            </li>
        </ul>

        <!-- 收藏弹窗 -->
        <div v-if="showModal" class="modal-overlay" @click="showModal = false">
            <div class="modal-content" @click.stop>
                <h3>选择收藏歌单</h3>
                <div v-if="myCollections.length === 0" class="empty-list">
                    暂无歌单，请先去"我的"页面创建
                </div>
                <ul v-else class="collection-list">
                    <li v-for="list in myCollections" :key="list.id" @click="confirmCollect(list.id)">
                        {{ list.title }}
                    </li>
                </ul>
                <button class="close-btn" @click="showModal = false">取消</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAllSongs } from '../../api/search'
import { getCollectionsList, addSongToCollection } from '../../api/collection'
import { showMessage } from '../../utils/message'

const emit = defineEmits(['play'])
const songs = ref([])
const loading = ref(true)
const error = ref(null)

// 收藏相关
const showModal = ref(false)
const myCollections = ref([])
const currentSongId = ref(null)

function formatDuration(seconds) {
    if (!seconds) return '0:00'
    const m = Math.floor(seconds / 60)
    const s = Math.floor(seconds % 60)
    return `${m}:${s.toString().padStart(2, '0')}`
}

async function openCollectModal(songId) {
    currentSongId.value = songId
    try {
        myCollections.value = await getCollectionsList()
        showModal.value = true
    } catch (e) {
        showMessage(e.message || '获取歌单失败', 'error')
    }
}

async function confirmCollect(listId) {
    try {
        await addSongToCollection(listId, currentSongId.value)
        showMessage('收藏成功', 'success')
        showModal.value = false
    } catch (e) {
        showMessage(e.message || '收藏失败', 'error')
    }
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

.actions {
    display: flex;
    gap: 10px;
}

.play-btn, .collect-btn {
    padding: 8px 16px;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.play-btn {
    background-color: #1890ff;
}

.play-btn:hover {
    background-color: #40a9ff;
}

.collect-btn {
    background-color: #ff4d4f;
}

.collect-btn:hover {
    background-color: #ff7875;
}

/* 弹窗样式 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 300px;
    max-height: 80vh;
    overflow-y: auto;
}

.collection-list {
    list-style: none;
    padding: 0;
    margin: 20px 0;
}

.collection-list li {
    padding: 10px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
}

.collection-list li:hover {
    background: #f5f5f5;
}

.close-btn {
    width: 100%;
    padding: 8px;
    background: #ddd;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.empty-list {
    text-align: center;
    color: #999;
    padding: 20px 0;
}
</style>
