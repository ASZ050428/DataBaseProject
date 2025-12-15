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
                        </div>
                        <button class="action-btn" @click="emit('play', song.audio_url)" style="margin-right: 10px;">▶ 播放</button>
                        <button class="action-btn">➕ 收藏</button>
                    </li>
                </ul>
            </div>

            <!-- 专辑结果 -->
            <div class="result-section">
                <h3>专辑</h3>
                <div v-if="albums.length === 0" class="empty-tip">未找到相关专辑</div>
                <ul v-else class="result-list">
                    <li v-for="album in albums" :key="album.album_id" class="result-item">
                        <div class="item-info">
                            <div class="item-title">{{ album.album_name }}</div>
                            <div class="item-sub">发行时间: {{ formatDate(album.release_time) }}</div>
                        </div>
                        <button class="action-btn">❤️ 收藏</button>
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
                        <button class="action-btn">❤️ 关注</button>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { searchSong, searchAlbum, searchArtist } from '../../api/search'

const emit = defineEmits(['play'])

const query = ref('')
const songs = ref([])
const albums = ref([])
const artists = ref([])
const hasSearched = ref(false)

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
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
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

.action-btn {
    padding: 6px 12px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
    margin-left: 10px;
}

.action-btn:hover {
    background-color: #f0f0f0;
    border-color: #ccc;
    color: #2563eb;
}

.empty-tip {
    color: #999;
    font-style: italic;
    padding: 10px 0;
}
</style>
