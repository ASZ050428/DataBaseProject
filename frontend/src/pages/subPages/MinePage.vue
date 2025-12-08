<template>
    <div class="mine-page">
        <h1>个人中心</h1>
        <nav class="mine-navbar">
            <ul class="nav-links">
                <li>
                    <div class="nav-item" @click="currentContent = 'favoriteSongsList'">收藏列表</div>
                </li>
                <li>
                    <div class="nav-item" @click="currentContent = 'favoriteAlbums'">专辑</div>
                </li>
                <li>
                    <div class="nav-item" @click="currentContent = 'favoriteArtists'">歌手</div>
                </li>
                <li>
                    <div class="nav-item" @click="currentContent = 'personalInfo'">个人信息</div>
                </li>
            </ul>
        </nav>
        <div v-if="currentContent != 'personalInfo'" class="favorites-section">
            <h2>我的收藏</h2>
            <div v-if="currentContent === 'favoriteSongsList'" class="fav-group">
                <!-- 列表模式 -->
                <div v-if="!currentCollectionId">
                    <div class="group-header">
                        <h3>收藏列表</h3>
                        <button class="add-list" @click="showAddListModal = true">添加收藏列表</button>
                    </div>
                    <div v-if="favoriteSongsList.length === 0" class="empty-tip">暂无收藏歌曲</div>
                    <ul v-else class="fav-list">
                        <li v-for="list in favoriteSongsList" :key="list.id" class="fav-item" @click="showCollectionList(list)">
                            <div class="fav-info">
                                <div class="fav-title">{{ list.title }}</div>
                            </div>
                            <button class="remove-btn" @click.stop="removeList(list.id)">💔</button>
                        </li>
                    </ul>
                </div>

                <!-- 详情模式 -->
                <div v-else>
                    <div class="group-header">
                        <div class="header-left">
                            <button class="back-btn" @click="backToCollections">返回</button>
                            <h3>{{ currentCollectionListName }}</h3>
                        </div>
                    </div>
                    <div v-if="currentCollectionListSongs.length === 0" class="empty-tip">此歌单暂无歌曲</div>
                    <ul v-else class="fav-list">
                        <li v-for="song in currentCollectionListSongs" :key="song.id" class="fav-item">
                            <div class="fav-info">
                                <div class="fav-title">{{ song.title }}</div>
                            </div>
                            <button class="remove-btn" @click="removeSongFromList(song.id)">💔</button>
                        </li>
                    </ul>
                </div>
            </div>
            <div v-if="currentContent === 'favoriteAlbums'" class="fav-group">
                <div class="group-header">
                    <h3>专辑</h3>
                </div>
                <div v-if="favoriteAlbums.length === 0" class="empty-tip">暂无收藏专辑</div>
                <ul v-else class="fav-list">
                    <li v-for="album in favoriteAlbums" :key="album.id" class="fav-item">
                        <div class="fav-info">
                            <div class="fav-title">{{ album.title }}</div>
                        </div>
                        <button class="remove-btn" @click="removeAlbum(album.id)">💔</button>
                    </li>
                </ul>
            </div>
            <div v-if="currentContent === 'favoriteArtists'" class="fav-group">
                <div class="group-header">
                    <h3>歌手</h3>
                </div>
                <div v-if="favoriteArtists.length === 0" class="empty-tip">暂无关注歌手</div>
                <ul v-else class="fav-list">
                    <li v-for="artist in favoriteArtists" :key="artist.id" class="fav-item">
                        <div class="fav-info">
                            <div class="fav-title">{{ artist.title }}</div>
                        </div>
                        <button class="remove-btn" @click="removeArtist(artist.id)">💔</button>
                    </li>
                </ul>
            </div>
        </div>
        <div v-if="currentContent === 'personalInfo'" class="info-section">
            <h2>修改个人信息</h2>
            <div class="info-item">
                <span class="label">用户名</span>
                <input type="text" v-model="username" placeholder="请输入新的用户名" />
                <button>保存</button>
            </div>
            <div class="info-item">
                <span class="label">密码</span>
                <input type="password" v-model="password" placeholder="请输入新的密码" />
                <button>保存</button>
            </div>
        </div>
    </div>

    <!-- 添加收藏列表的弹窗 -->
    <div v-if="showAddListModal" class="modal-overlay" @click.self="showAddListModal = false">
        <div class="modal-content">
            <h3>添加收藏列表</h3>
            <input v-model="newListName" placeholder="请输入列表名称" class="modal-input" />
            <div class="modal-actions">
                <button @click="addList" class="confirm-btn">确认添加</button>
                <button @click="showAddListModal = false" class="cancel-btn">取消</button>
            </div>
        </div>
    </div>

    <!-- 确认删除弹窗 -->
    <div v-if="showConfirmWindow" class="modal-overlay" @click.self="showConfirmWindow = false">
        <div class="modal-content">
            <h3>确认删除？</h3>
            <div class="modal-delete-actions">
                <button @click="confirmDelete" class="confirm-btn">确认</button>
                <button @click="showConfirmWindow = false" class="cancel-btn">取消</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
    getCollectionsList, 
    addCollection, 
    deleteCollection,
    getFavoriteAlbums, 
    removeFavoriteAlbum,
    getFavoriteArtists, 
    removeFavoriteArtist,
    getCollectionListSongs
} from '../../api/collection'

const currentContent = ref('favoriteSongsList')
const username = ref('')
const password = ref('')
// 控制弹窗显示
const showAddListModal = ref(false)
const showConfirmWindow = ref(false)
// 新收藏列表名称
const newListName = ref('')
// 待删除项
const pendingDelete = ref(null)
// 当前选中的收藏列表名称
const currentCollectionListName = ref('')
const currentCollectionId = ref(null)

// 收藏数据 (初始化为空数组，防止页面报错)
const favoriteSongsList = ref([])
const favoriteAlbums = ref([])
const favoriteArtists = ref([])
const currentCollectionListSongs = ref([])

// 页面加载时读取用户信息及收藏数据
onMounted(async () => {
    try {
        const userStr = localStorage.getItem('user')
        if (userStr) {
            const user = JSON.parse(userStr)
            username.value = user.username || ''
            password.value = user.password || ''
        }
        
        // 并行加载所有数据
        const [listsData, albumsData, artistsData] = await Promise.all([
            getCollectionsList(),
            getFavoriteAlbums(),
            getFavoriteArtists()
        ])

        favoriteSongsList.value = listsData || []
        favoriteAlbums.value = albumsData || []
        favoriteArtists.value = artistsData || []

    } catch (e) {
        console.error('加载数据失败', e)
    }
})

// 添加收藏列表
async function addList() {
    if (!newListName.value.trim()) {
        alert('请输入列表名称')
        return
    }
    
    try {
        // 1. 提交到后端
        const newList = await addCollection(newListName.value)
        
        // 2. 后端返回成功后，直接添加到本地列表头部 (无需重新获取整个列表)
        favoriteSongsList.value.unshift(newList)
        
        newListName.value = '' // 清空输入框
        showAddListModal.value = false // 关闭弹窗
    } catch (e) {
        alert(e.message || '添加失败')
    }
}

// 显示歌单歌曲内容
async function showCollectionList(list) {
    try {
        currentCollectionListName.value = list.title
        currentCollectionId.value = list.id
        const songs = await getCollectionListSongs(list.id)
        currentCollectionListSongs.value = songs || []
    } catch (e) {
        alert(e.message || '加载歌单歌曲失败')
    }
}

function backToCollections() {
    currentCollectionId.value = null
    currentCollectionListSongs.value = []
    currentCollectionListName.value = ''
}

function removeSongFromList(songId) {
    // TODO: 待实现移除功能
    alert('移除歌曲功能开发中...')
}


function removeList(id) {
    pendingDelete.value = { type: 'list', id }
    showConfirmWindow.value = true
}

function removeAlbum(id) {
    pendingDelete.value = { type: 'album', id }
    showConfirmWindow.value = true
}

function removeArtist(id) {
    pendingDelete.value = { type: 'artist', id }
    showConfirmWindow.value = true
}

async function confirmDelete() {
    if (!pendingDelete.value) return
    
    const { type, id } = pendingDelete.value
    try {
        if (type === 'list') {
            await deleteCollection(id)
            favoriteSongsList.value = favoriteSongsList.value.filter(item => item.id !== id)
        } else if (type === 'album') {
            await removeFavoriteAlbum(id)
            favoriteAlbums.value = favoriteAlbums.value.filter(item => item.id !== id)
        } else if (type === 'artist') {
            await removeFavoriteArtist(id)
            favoriteArtists.value = favoriteArtists.value.filter(item => item.id !== id)
        }
        showConfirmWindow.value = false
        pendingDelete.value = null
    } catch (e) {
        alert(e.message || '删除失败')
    }
}
</script>

<style scoped>
.mine-page {
    padding: 24px;
    background: #fff;
    /* text-align: center;  <-- 去掉这个，让整体左对齐更自然 */
}

.mine-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #2a3d51; /* 深蓝灰色，比纯黑更有质感 */
    border-radius: 10px;
    color: white;
    padding: 1rem 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* 加一点阴影，增加立体感 */
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 20px;
    padding: 0;
    margin: 0;
}

.nav-links .nav-item {
    color: white;
    text-decoration: none;
    font-size: 1rem;
    padding: 5px 10px;
    border-radius: 4px;
    transition: background-color 0.3s;
    cursor: pointer;
}

.nav-links .nav-item:hover {
    color: #ddd;
    background-color: rgba(255, 255, 255, 0.1);
}

.favorites-section {
    margin-top: 20px;
    text-align: left;
    margin-left: 30px;
    margin-right: 30px;
    /* 限制宽度，防止列表太宽 */
}

.fav-group h3 {
    font-size: 18px;
    color: #555;
    margin: 0;
    /* 去掉默认 margin，由父容器控制 */
}

.group-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    border-bottom: 2px solid #f0f0f0;
    padding-bottom: 10px;
}

.add-list {
    padding: 6px 14px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    /* 字体稍微改小一点，更协调 */
    cursor: pointer;
    transition: background-color 0.3s;
}

.add-list:hover {
    background-color: #45a049;
    /* 悬停加深 */
}

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
    /* 悬停微微上浮 */
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

.remove-btn {
    background: none;
    border: none;
    font-size: 18px;
    cursor: pointer;
    padding: 8px;
    border-radius: 50%;
    transition: background-color 0.3s;
}

.remove-btn:hover {
    background-color: #ffebee;
    /* 悬停时显示浅红色背景 */
}

.empty-tip {
    color: #999;
    font-style: italic;
    padding: 20px 0;
}

.info-section {
    margin-top: 30px;
    text-align: left;
    margin-left: 30px;
}

.info-item {
    display: flex;
    align-items: center;
    /* 垂直居中对齐 */
    gap: 12px;
    max-width: 500px;
    /* 限制最大宽度，防止太长 */
    margin-top: 15px;
}

.label {
    font-weight: bold;
    color: #333;
    min-width: 60px;
    /* 给标签一个最小宽度，对齐更好看 */
}

.info-item input {
    flex: 1;
    /* 让输入框自动填满剩余空间 */
    padding: 8px 12px;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
}

.info-item input:focus {
    border-color: #2563eb;
    /* 聚焦时变蓝 */
}

.info-item button {
    padding: 6px 14px;
    background-color: #3cc0ef;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    /* 字体稍微改小一点，更协调 */
    cursor: pointer;
    transition: background-color 0.3s;
    white-space: nowrap;
    /* 防止按钮文字换行 */
}

.info-item button:hover {
    background-color: #3298eb;
    /* 悬停加深 */
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
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.modal-content h3 {
    margin: 0;
    color: #333;
    text-align: center;
}

.modal-input {
    padding: 10px;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
}

.modal-input:focus {
    border-color: #2563eb;
}

.modal-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
}

.modal-delete-actions {
    display: flex;
    gap: 12px;
    justify-content: center;
}

.modal-actions button,
.modal-delete-actions button {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.confirm-btn {
    background-color: #4caf50;
    color: white;
}

.confirm-btn:hover {
    background-color: #45a049;
}

.cancel-btn {
    background-color: #f5f5f5;
    color: #666;
}

.cancel-btn:hover {
    background-color: #e0e0e0;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 15px;
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
</style>