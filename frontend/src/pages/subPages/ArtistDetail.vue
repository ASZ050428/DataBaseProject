<template>
    <div class="artist-detail-page">
        <button class="back-btn" @click="$emit('back')">返回列表</button>

        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else class="content">
            <div class="header">
                <h1>{{ artist.artist_name }}</h1>
                <p class="region">地区: {{ artist.region || '未知' }}</p>
                <p class="song-count" style="color: #666; margin-top: 5px;">热门歌曲: {{ artist.song_count || 0 }} 首</p>
                <p class="bio">{{ artist.bio || '暂无简介' }}</p>
            </div>

            <div class="section">
                <h2>热门歌曲</h2>
                <div v-if="!artist.songs || artist.songs.length === 0" class="empty">暂无歌曲</div>
                <ul v-else class="fav-list">
                    <SongListItem 
                        v-for="song in artist.songs" 
                        :key="song.song_id" 
                        :song="song"
                        @play="$emit('play', $event)"
                        @collect="openCollectModal"
                        @comment="openCommentModal"
                    />
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
import { getArtistDetail } from '../../api/search'
import { useSongOperations } from '../../composables/useSongOperations'
import SongListItem from '../../components/SongListItem.vue'
import SongActionModals from '../../components/SongActionModals.vue'

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
    margin-bottom: 20px;
}

.back-btn:hover {
    background-color: #c0392b;
}

.header {
    margin-bottom: 30px;
    border-bottom: 1px solid #eee;
    padding-bottom: 20px;
}

.header h1 {
    margin: 0 0 10px 0;
    color: #333;
}

.region {
    color: #666;
    margin: 5px 0;
}

.bio {
    color: #888;
    line-height: 1.6;
    margin-top: 10px;
}

.section {
    margin-bottom: 40px;
}

.section h2 {
    font-size: 20px;
    color: #333;
    margin-bottom: 20px;
    border-left: 4px solid #ed3a3a;
    padding-left: 10px;
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

/* 专辑网格样式 */
.album-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    list-style: none;
    padding: 0;
}

.album-card {
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: transform 0.3s;
    padding: 15px;
    border: 1px solid #eee;
}

.album-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
}

.album-info h3 {
    margin: 0 0 5px 0;
    font-size: 16px;
    color: #333;
}

.release-time {
    font-size: 12px;
    color: #999;
    margin: 0;
}

.empty {
    color: #999;
    text-align: center;
    padding: 40px 0;
}

.loading,
.error {
    text-align: center;
    color: #666;
    padding: 20px;
}

.error {
    color: #ff4d4f;
}
</style>
