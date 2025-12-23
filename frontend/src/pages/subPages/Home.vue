<template>
    <div class="home-page">
        <h1>发现音乐</h1>
        <div class="search-container">
            <div class="search-box">
                <input 
                    type="text" 
                    placeholder="搜索歌曲、专辑、歌手..." 
                    v-model="query" 
                    @keyup.enter="search"
                />
                <button @click="search">搜索</button>
            </div>
        </div>

        <!-- 搜索结果区域 -->
        <div v-if="hasSearched" class="results-container">
            
            <!-- 歌曲结果 -->
            <div class="result-section">
                <h3>歌曲</h3>
                <div v-if="songs.length === 0" class="empty-tip">未找到相关歌曲</div>
                <ul v-else class="result-list">
                    <li v-for="song in songs" :key="song.song_id" class="result-item">
                        <div class="item-info">
                            <div class="item-title">{{ song.title }}</div>
                            <div class="item-sub">时长: {{ formatDuration(song.duration) }}</div>
                            <div class="item-sub">歌手: {{ song.artist_name }}</div>
                        </div>
                        <div class="item-actions">
                            <button class="action-btn btn-play" @click="emit('play', song.audio_url)">▶ 播放</button>
                            <button class="action-btn btn-collect" @click="openCollectModal(song.song_id)">❤ 收藏</button>
                            <button class="action-btn btn-comment" @click="openCommentModal(song.song_id)">💬 评论</button>
                        </div>
                    </li>
                </ul>
            </div>

            <!-- 专辑结果 -->
            <div class="result-section">
                <h3>专辑</h3>
                <div v-if="albums.length === 0" class="empty-tip">未找到相关专辑</div>
                <ul v-else class="result-list">
                    <li v-for="album in albums" :key="album.album_id" class="result-item" @click="$emit('select-album', album.album_id)">
                        <div class="item-info">
                            <div class="item-title">{{ album.album_name }}</div>
                            <div class="item-sub">发行时间: {{ formatDate(album.release_time) }}</div>
                        </div>
                        <button class="action-btn btn-collect" @click="handleCollectAlbum(album.album_id)">❤ 收藏</button>
                    </li>
                </ul>
            </div>

            <!-- 歌手结果 -->
            <div class="result-section">
                <h3>歌手</h3>
                <div v-if="artists.length === 0" class="empty-tip">未找到相关歌手</div>
                <ul v-else class="result-list">
                    <li v-for="artist in artists" :key="artist.id" class="result-item">
                        <div class="item-info">
                            <div class="item-title">{{ artist.artist_name }}</div>
                            <div class="item-sub">地区: {{ artist.region }}</div>
                        </div>
                        <button class="action-btn btn-follow" @click="handleFollowArtist(artist.artist_id)">＋ 关注</button>
                    </li>
                </ul>
            </div>
        </div>

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

        <!-- 评论弹窗 -->
        <div v-if="showCommentModal" class="modal-overlay" @click="showCommentModal = false">
            <div class="modal-content comment-modal" @click.stop>
                <h3>歌曲评论</h3>
                <div class="comment-list-container">
                    <div v-if="commentsLoading" class="loading-tip">加载中...</div>
                    <div v-else-if="comments.length === 0" class="empty-tip">暂无评论，快来抢沙发吧~</div>
                    <ul v-else class="comment-list">
                        <li v-for="comment in comments" :key="comment.id" class="comment-item">
                            <div class="comment-header">
                                <span class="comment-user">{{ comment.username }}</span>
                                <span class="comment-time">{{ formatDate(comment.create_time) }}</span>
                            </div>
                            <div class="comment-content">{{ comment.content }}</div>
                        </li>
                    </ul>
                </div>
                <div class="comment-input-area">
                    <textarea v-model="commentContent" placeholder="写下你的评论..." rows="3"></textarea>
                    <div class="modal-footer">
                        <button class="close-modal-btn" @click="showCommentModal = false">关闭</button>
                        <button class="submit-btn" @click="submitComment" :disabled="!commentContent.trim()">发表评论</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { showMessage } from '../../utils/message'
import { ref } from 'vue'
import { searchSong, searchAlbum, searchArtist } from '../../api/search'
import { 
    getCollectionsList, 
    addSongToCollection, 
    addFavoriteAlbum, 
    addFavoriteArtist 
} from '../../api/collection'
import { getSongComments, postComment } from '../../api/comment'

const emit = defineEmits(['play', 'select-album'])

const query = ref('')
const songs = ref([])
const albums = ref([])
const artists = ref([])
const hasSearched = ref(false)

// 评论相关状态
const showCommentModal = ref(false)
const comments = ref([])
const commentContent = ref('')
const currentSongId = ref(null)
const commentsLoading = ref(false)

// 收藏相关状态
const showModal = ref(false)
const myCollections = ref([])
const targetSongId = ref(null)

async function openCollectModal(songId) {
    targetSongId.value = songId
    try {
        const list = await getCollectionsList()
        myCollections.value = Array.isArray(list) ? list : []
        showModal.value = true
    } catch (e) {
        showMessage(e.message || '获取歌单失败', 'error')
    }
}

async function handleCollectAlbum(albumId) {
    try {
        await addFavoriteAlbum(albumId)
        showMessage('专辑收藏成功！', 'success')
    } catch (e) {
        showMessage(e.message || '收藏失败', 'error')
    }
}

async function handleFollowArtist(artistId) {
    try {
        await addFavoriteArtist(artistId)
        showMessage('关注成功！', 'success')
    } catch (e) {
        showMessage(e.message || '关注失败', 'error')
    }
}

async function confirmCollect(listId) {
    if (!targetSongId.value) return
    try {
        await addSongToCollection(listId, targetSongId.value)
        showMessage('收藏成功！', 'success')
        showModal.value = false
    } catch (e) {
        showMessage(e.message || '收藏失败', 'error')
    }
}

async function openCommentModal(songId) {
    currentSongId.value = songId
    showCommentModal.value = true
    commentContent.value = ''
    await loadComments(songId)
}

async function loadComments(songId) {
    commentsLoading.value = true
    try {
        const res = await getSongComments(songId)
        comments.value = Array.isArray(res) ? res : []
    } catch (e) {
        showMessage(e.message || '加载评论失败', 'error')
    } finally {
        commentsLoading.value = false
    }
}

async function submitComment() {
    if (!commentContent.value.trim()) return
    
    try {
        await postComment(currentSongId.value, commentContent.value)
        showMessage('评论成功！', 'success')
        commentContent.value = ''
        await loadComments(currentSongId.value)
    } catch (e) {
        showMessage(e.message || '评论失败', 'error')
    }
}

async function search() {
    if (!query.value.trim()) return
    
    try {
        hasSearched.value = true
        // 使用 Promise.allSettled 防止某个接口报错导致所有结果都不显示
        const results = await Promise.allSettled([
            searchSong(query.value),
            searchAlbum(query.value),
            searchArtist(query.value)
        ])
        
        // results[0] 是歌曲, results[1] 是专辑, results[2] 是歌手
        songs.value = results[0].status === 'fulfilled' ? results[0].value : []
        albums.value = results[1].status === 'fulfilled' ? results[1].value : []
        artists.value = results[2].status === 'fulfilled' ? results[2].value : []

        // 如果有错误，打印出来方便调试
        if (results[0].status === 'rejected') console.error('搜索歌曲失败:', results[0].reason)
        if (results[1].status === 'rejected') console.error('搜索专辑失败:', results[1].reason)
        if (results[2].status === 'rejected') console.error('搜索歌手失败:', results[2].reason)
        
    } catch (error) {
        console.error('搜索流程出错:', error)
    }
}

function formatDuration(seconds) {
    if (!seconds) return '0:00'
    const min = Math.floor(seconds / 60)
    const sec = seconds % 60
    return `${min}:${sec.toString().padStart(2, '0')}`
}

function formatDate(dateStr) {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString()
}
</script>

<style scoped>
.home-page {
    padding: 24px;
    background: #fff;
    min-height: 100%;
}

h1 {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
}

.search-container {
    display: flex;
    justify-content: center;
    margin-bottom: 40px;
}

.search-box {
    display: flex;
    gap: 10px;
    width: 100%;
    max-width: 600px;
}

.search-box input {
    flex: 1;
    padding: 12px 20px;
    border: 2px solid #e0e0e0;
    border-radius: 25px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
}

.search-box input:focus {
    border-color: #2563eb;
}

/* 弹窗样式 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
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

.modal-content h3 {
    margin-top: 0;
    text-align: center;
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

.search-box button {
    padding: 10px 30px;
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 25px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
    white-space: nowrap;
}

.search-box button:hover {
    background-color: #1d4ed8;
}

.results-container {
    max-width: 1000px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.result-section h3 {
    font-size: 20px;
    color: #333;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #f0f0f0;
}

.result-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 15px;
}

.result-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    background: #f9f9f9;
    border-radius: 8px;
    transition: transform 0.2s, box-shadow 0.2s;
}

.result-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    background: #fff;
}

.item-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
    overflow: hidden;
    flex: 1;
    min-width: 0;
    margin-right: 10px;
}

.item-title {
    font-weight: bold;
    font-size: 16px;
    color: #333;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.item-sub {
    font-size: 13px;
    color: #666;
}

.item-actions {
    display: flex;
    gap: 10px;
    flex-shrink: 0;
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

.btn-play {
    background-color: #ebf2ff;
    color: #2563eb;
}
.btn-play:hover {
    background-color: #2563eb;
    color: white;
}

.btn-collect {
    background-color: #fff0f0;
    color: #ef4444;
}
.btn-collect:hover {
    background-color: #ef4444;
    color: white;
}

.btn-follow {
    background-color: #f0fdf4;
    color: #16a34a;
}
.btn-follow:hover {
    background-color: #16a34a;
    color: white;
}

.btn-comment {
    background-color: #f3f4f6;
    color: #4b5563;
}
.btn-comment:hover {
    background-color: #4b5563;
    color: white;
}

.empty-tip {
    color: #999;
    font-style: italic;
    margin-left: 25px;
    padding: 10px 0;
}

.loading-tip {
    text-align: center;
    padding: 40px 0;
    color: #6b7280;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.loading-tip::before {
    content: "";
    width: 16px;
    height: 16px;
    border: 2px solid #e5e7eb;
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* 评论模态框样式 */
.comment-modal {
    width: 550px;
    max-width: 90vw;
    display: flex;
    flex-direction: column;
    max-height: 85vh;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    padding: 0;
    overflow: hidden;
    background: #fff;
}

.comment-modal h3 {
    margin: 0;
    padding: 20px 24px;
    font-size: 18px;
    font-weight: 600;
    color: #1f2937;
    border-bottom: 1px solid #f3f4f6;
    background: #fff;
    text-align: left;
}

.comment-list-container {
    flex: 1;
    overflow-y: auto;
    padding: 0;
    background: #fff;
    margin: 0;
    border: none;
}

/* 滚动条美化 */
.comment-list-container::-webkit-scrollbar {
    width: 6px;
}
.comment-list-container::-webkit-scrollbar-thumb {
    background-color: #e5e7eb;
    border-radius: 3px;
}

.comment-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.comment-item {
    padding: 20px 24px;
    border-bottom: 1px solid #f3f4f6;
    transition: background-color 0.2s;
}

.comment-item:last-child {
    border-bottom: none;
}

.comment-item:hover {
    background-color: #f9fafb;
}

.comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.comment-user {
    font-weight: 600;
    font-size: 14px;
    color: #374151;
}

.comment-time {
    font-size: 12px;
    color: #9ca3af;
}

.comment-content {
    font-size: 14px;
    color: #4b5563;
    line-height: 1.6;
    white-space: pre-wrap;
}

.comment-input-area {
    padding: 20px 24px;
    background: #fff;
    border-top: 1px solid #f3f4f6;
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin: 0;
}

.comment-input-area textarea {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    resize: none;
    font-family: inherit;
    font-size: 14px;
    background-color: #f9fafb;
    transition: all 0.2s;
    outline: none;
    box-sizing: border-box;
}

.comment-input-area textarea:focus {
    background-color: #fff;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    align-items: center;
}

.submit-btn {
    padding: 8px 24px;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
    align-self: auto;
}

.submit-btn:hover {
    background-color: #2563eb;
}

.submit-btn:disabled {
    background-color: #93c5fd;
    cursor: not-allowed;
}

.close-modal-btn {
    padding: 8px 20px;
    background-color: transparent;
    color: #6b7280;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
}

.close-modal-btn:hover {
    background-color: #f3f4f6;
    color: #374151;
}
</style>
