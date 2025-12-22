<template>
    <div class="album-detail-page">
        <button class="back-btn" @click="$emit('back')">返回列表</button>

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
                <ul v-else class="fav-list">
                    <li v-for="song in album.songs" :key="song.song_id" class="fav-item">
                        <div class="fav-info">
                            <div class="fav-title">{{ song.title }}</div>
                            <div class="fav-meta">{{ formatDuration(song.duration) }}</div>
                        </div>
                        <div class="actions">
                            <button class="action-btn play-btn" @click="$emit('play', song.audio_url)" title="播放">
                                ▶ 播放
                            </button>
                            <button class="action-btn fav-btn" @click="openAddToCollectionModal(song.song_id)"
                                title="收藏">
                                ❤ 收藏
                            </button>
                        </div>
                    </li>
                </ul>
            </div>
        </div>

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
import { ref, onMounted, watch } from 'vue'
import { getAlbumDetail } from '../../api/search'
import { getCollectionsList, addSongToCollection } from '../../api/collection'
import { showMessage } from '../../utils/message'

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

onMounted(loadData)
watch(() => props.albumId, loadData)
</script>

<style scoped>
.album-detail-page {
    background: #fff;
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

/* 歌曲列表样式 - 仿照 FavoriteSongs.vue */
.fav-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.fav-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 15px;
    background: #f9f9f9;
    border-radius: 8px;
    margin-bottom: 10px;
    transition: transform 0.2s, box-shadow 0.2s;
}

.fav-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    background: #fff;
}

.fav-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.fav-title {
    font-weight: bold;
    font-size: 16px;
    color: #333;
}

.fav-meta {
    font-size: 12px;
    color: #999;
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
    color: #666;
    padding: 20px;
}

.error {
    color: #ff4d4f;
}
</style>
