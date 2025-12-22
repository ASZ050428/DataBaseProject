<template>
    <div class="song-list-page">
        <h1>歌曲列表</h1>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="songs.length === 0" class="empty">暂无歌曲</div>
        <ul v-else class="song-list">
            <SongListItem 
                v-for="song in songs" 
                :key="song.song_id" 
                :song="song"
                @play="$emit('play', $event)"
                @collect="openCollectModal"
                @comment="openCommentModal"
            />
        </ul>

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
import { ref, onMounted } from 'vue'
import { getAllSongs } from '../../api/search'
import { useSongOperations } from '../../composables/useSongOperations'
import SongListItem from '../../components/SongListItem.vue'
import SongActionModals from '../../components/SongActionModals.vue'

const emit = defineEmits(['play'])
const songs = ref([])
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
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.loading,
.error,
.empty {
    text-align: center;
    color: #999;
    padding: 20px 0;
}
</style>
