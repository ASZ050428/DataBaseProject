<template>
    <div class="album-detail-page">
        <button class="back-btn" @click="$emit('back')">返回列表</button>

        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else class="content">
            <div class="header">
                <h1>{{ album.album_name }}</h1>
                <p class="meta">发行时间: {{ album.release_time }}</p>
                <p class="meta">歌手: {{ album.artist_name }}</p>
                <p class="meta">歌曲: {{ album.song_count || 0 }} 首</p>
            </div>

            <div class="section">
                <h2>歌曲列表</h2>
                <div v-if="!album.songs || album.songs.length === 0" class="empty">该专辑暂无歌曲</div>
                <ul v-else class="fav-list">
                    <SongListItem 
                        v-for="song in album.songs" 
                        :key="song.song_id" 
                        :song="song"
                        @play="$emit('play', $event)"
                        @collect="openCollectModal"
                        @comment="openCommentModal"
                    />
                </ul>
            </div>
        </div>

        <!-- 弹窗组件 -->
        <SongActionModals 
            :collect-visible="collectModalVisible"
            :comment-visible="commentModalVisible"
            :collections="userCollections"
            :collections-loading="collectionsLoading"
            :comments="comments"
            :comments-loading="commentsLoading"
            :comment-content="commentContent"
            @close="closeModals"
            @add-to-collection="addToCollection"
            @submit-comment="submitComment"
            @update:commentContent="commentContent = $event"
        />
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { getAlbumDetail } from '../../api/search'
import { useSongOperations } from '../../composables/useSongOperations'
import SongListItem from '../../components/SongListItem.vue'
import SongActionModals from '../../components/SongActionModals.vue'

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

// 使用组合式函数
const {
    collectModalVisible,
    commentModalVisible,
    userCollections,
    collectionsLoading,
    comments,
    commentsLoading,
    commentContent,
    openCollectModal,
    addToCollection,
    openCommentModal,
    submitComment,
    closeModals
} = useSongOperations()

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

/* 歌曲列表样式 - 仿照 FavoriteSongs.vue */
.fav-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
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
