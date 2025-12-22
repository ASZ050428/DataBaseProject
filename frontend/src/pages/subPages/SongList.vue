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
                    <button class="action-btn play-btn" @click="$emit('play', song.audio_url)" title="播放">
                        ▶ 播放
                    </button>
                    <button class="action-btn fav-btn" @click="openAddToCollectionModal(song.song_id)" title="收藏">
                        ❤ 收藏
                    </button>
                </div>
            </li>
        </ul>

        <!-- 添加到歌单弹窗 -->
        <div v-if="showAddToCollectionModal" class="modal-overlay" @click.self="closeAddToCollectionModal">
            <div class="modal-content">
                <h3>添加到歌单</h3>
                <div v-if="collectionsLoading" class="loading-tip">加载歌单中...</div>
                <div v-else-if="userCollections.length === 0" class="empty-tip">
                    暂无歌单，请先去"我的"页面创建歌单
                </div>
                <ul v-else class="collection-select-list">
                    <li v-for="list in userCollections" :key="list.id" class="collection-select-item"
                        @click="addToCollection(list.id)">
                        {{ list.title }}
                    </li>
                </ul>
                <button class="cancel-btn" @click="closeAddToCollectionModal">取消</button>
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

const showAddToCollectionModal = ref(false)
const userCollections = ref([])
const collectionsLoading = ref(false)
const selectedSongId = ref(null)

// 打开收藏弹窗
async function openAddToCollectionModal(songId) {
    selectedSongId.value = songId
    showAddToCollectionModal.value = true
    collectionsLoading.value = true
    try {
        const lists = await getCollectionsList()
        userCollections.value = lists || []
    } catch (e) {
        showMessage('获取歌单列表失败', 'error')
    } finally {
        collectionsLoading.value = false
    }
}

function closeAddToCollectionModal() {
    showAddToCollectionModal.value = false
    selectedSongId.value = null
    userCollections.value = []
}

// 添加歌曲到歌单
async function addToCollection(listId) {
    if (!selectedSongId.value) return

    try {
        await addSongToCollection(listId, selectedSongId.value)
        showMessage('收藏成功', 'success')
        closeAddToCollectionModal()
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
    background: #fff;
    padding: 20px;
}

.song-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.song-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 15px;
    background: #f9f9f9;
    border-radius: 8px;
    margin-bottom: 10px;
    transition: transform 0.2s, box-shadow 0.2s;
}

.song-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    background: #fff;
}

.song-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.song-title {
    font-weight: bold;
    font-size: 16px;
    color: #333;
}

.song-meta {
    font-size: 12px;
    color: #999;
}

.song-meta span {
    margin-right: 15px;
}

.actions {
    display: flex;
    gap: 10px;
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
    gap: 4px;
}

.play-btn {
    background-color: #ebf2ff;
    color: #2563eb;
}

.play-btn:hover {
    background-color: #2563eb;
    color: white;
}

.fav-btn {
    background-color: #fff0f0;
    color: #ef4444;
}

.fav-btn:hover {
    background-color: #ef4444;
    color: white;
}

/* 弹窗样式 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 24px;
    border-radius: 12px;
    width: 400px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.modal-content h3 {
    margin: 0;
    color: #333;
    text-align: center;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.collection-select-list {
    list-style: none;
    padding: 0;
    margin: 0;
    max-height: 300px;
    overflow-y: auto;
}

.collection-select-item {
    padding: 12px;
    border-bottom: 1px solid #f5f5f5;
    cursor: pointer;
    transition: background-color 0.2s;
    border-radius: 4px;
}

.collection-select-item:hover {
    background-color: #f0f7ff;
    color: #1976d2;
}

.cancel-btn {
    padding: 10px;
    background-color: #f5f5f5;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    color: #666;
    transition: background-color 0.2s;
}

.cancel-btn:hover {
    background-color: #e0e0e0;
}

.loading-tip,
.empty-tip {
    text-align: center;
    color: #999;
    padding: 20px;
}

.loading,
.error,
.empty {
    text-align: center;
    color: #999;
    padding: 20px 0;
}
</style>
