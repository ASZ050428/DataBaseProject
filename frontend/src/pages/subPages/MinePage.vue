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
                <li v-if="isArtist">
                    <div class="nav-item" @click="currentContent = 'creatorCenter'">创作者中心</div>
                </li>
            </ul>
        </nav>
        <div v-if="currentContent != 'personalInfo'" class="favorites-section">
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
                            <div class="fav-info" @click="emit('play', song.audio_url)" style="cursor: pointer;" title="点击播放">
                                <div class="fav-title">▶ {{ song.title }}</div>
                            </div>
                            <div class="actions" style="display: flex; gap: 10px; align-items: center;">
                                <button @click="emit('play', song.audio_url)" style="padding: 4px 8px; font-size: 12px; cursor: pointer;">▶ 播放</button>
                                <button class="remove-btn" @click="removeSongFromList(song.id)">💔</button>
                            </div>
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
                        <div class="fav-info" @click="emit('select-album', album.id)" style="cursor: pointer">
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
                        <div class="fav-info" @click="emit('select-artist', artist.id)" style="cursor: pointer" title="点击查看歌手详情">
                            <div class="fav-title">{{ artist.title }}</div>
                        </div>
                        <button class="remove-btn" @click="removeArtist(artist.id)">💔</button>
                    </li>
                </ul>
            </div>

            <!-- Creator Center Content -->
            <div v-if="currentContent === 'creatorCenter'" class="fav-group">
                <div class="group-header">
                    <h3>创作者中心</h3>
                    <div class="creator-actions" style="display: flex; gap: 10px;">
                        <button class="add-list" @click="showUploadModal = true">发布歌曲</button>
                        <button class="add-list" @click="showCreateAlbumModal = true">发布专辑</button>
                    </div>
                </div>
                
                <div class="sub-nav" style="margin-bottom: 20px; display: flex; gap: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px;">
                    <span @click="creatorContent = 'publishedSongs'" style="cursor: pointer; padding: 5px 10px;" :style="creatorContent === 'publishedSongs' ? 'font-weight: bold; color: #4caf50; border-bottom: 2px solid #4caf50;' : ''">已发布歌曲</span>
                    <span @click="creatorContent = 'publishedAlbums'" style="cursor: pointer; padding: 5px 10px;" :style="creatorContent === 'publishedAlbums' ? 'font-weight: bold; color: #4caf50; border-bottom: 2px solid #4caf50;' : ''">已发布专辑</span>
                    <span @click="creatorContent = 'artistProfile'" style="cursor: pointer; padding: 5px 10px;" :style="creatorContent === 'artistProfile' ? 'font-weight: bold; color: #4caf50; border-bottom: 2px solid #4caf50;' : ''">歌手信息</span>
                </div>

                <div v-if="creatorContent === 'publishedSongs'">
                     <div v-if="mySongs.length === 0" class="empty-tip">暂无发布歌曲</div>
                     <ul v-else class="fav-list">
                        <li v-for="song in mySongs" :key="song.song_id" class="fav-item">
                            <div class="fav-info">
                                <div class="fav-title">{{ song.title }}</div>
                                <div class="fav-sub" style="font-size: 12px; color: #888;">{{ song.album_title ? `专辑: ${song.album_title}` : '未归属专辑' }}</div>
                            </div>
                            <div class="actions" style="display: flex; gap: 10px; align-items: center;">
                                <button @click="emit('play', song.audio_url)" style="padding: 4px 8px; font-size: 12px; cursor: pointer;">▶ 播放</button>
                                <button @click="openAddToAlbum(song)" style="padding: 4px 8px; font-size: 12px; cursor: pointer;">管理专辑</button>
                                <button class="remove-btn" @click="handleDeleteSong(song.song_id)">🗑️</button>
                            </div>
                        </li>
                    </ul>
                </div>

                <div v-if="creatorContent === 'publishedAlbums'">
                    <div v-if="myAlbums.length === 0" class="empty-tip">暂无发布专辑</div>
                    <ul v-else class="fav-list">
                        <li v-for="album in myAlbums" :key="album.album_id" class="fav-item">
                            <div class="fav-info" @click="emit('select-album', album.album_id)" style="cursor: pointer" title="点击查看专辑详情">
                                <div class="fav-title">{{ album.album_name }}</div>
                                <div class="fav-sub" style="font-size: 12px; color: #888;">发布于: {{ album.release_time }}</div>
                            </div>
                            <div class="actions" style="display: flex; gap: 10px; align-items: center;">
                                <button @click="openManageAlbumContent(album)" style="padding: 4px 8px; font-size: 12px; cursor: pointer;">管理内容</button>
                                <button class="remove-btn" @click="handleDeleteAlbum(album.album_id)">🗑️</button>
                            </div>
                        </li>
                    </ul>
                </div>

                <div v-if="creatorContent === 'artistProfile'" class="info-section" style="margin: 0;">
                    <div class="info-item">
                        <span class="label">歌手名称</span>
                        <input type="text" v-model="artistProfile.name" placeholder="请输入歌手名称" />
                    </div>
                    <div class="info-item">
                        <span class="label">地区</span>
                        <input type="text" v-model="artistProfile.region" placeholder="请输入地区" />
                    </div>
                    <div class="info-item" style="align-items: flex-start;">
                        <span class="label" style="margin-top: 8px;">简介</span>
                        <textarea v-model="artistProfile.bio" placeholder="请输入简介" style="flex: 1; padding: 8px 12px; border: 2px solid #e0e0e0; border-radius: 6px; font-size: 16px; outline: none; min-height: 100px; resize: vertical; font-family: inherit;"></textarea>
                    </div>
                    <div class="info-item">
                        <button @click="saveArtistProfile">保存修改</button>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="currentContent === 'personalInfo'" class="info-section">
            <h2>修改个人信息</h2>
            <div class="info-item">
                <span class="label">用户名</span>
                <input type="text" v-model="username" placeholder="请输入新的用户名" />
                <button @click="changeUserName">保存</button>
            </div>
            <div class="info-item">
                <button @click="isChangingPassword = true" >更改密码</button>
            </div>
            
            <!-- 升级歌手入口 -->
            <div class="upgrade-section" v-if="!isArtist">
                <div class="divider"></div>
                <h3>成为创作者</h3>
                <p class="upgrade-desc">升级为歌手账号，发布属于你的音乐作品</p>
                <button class="upgrade-btn" @click="showUpgradeModal = true; artistName = username">立即升级</button>
            </div>
        </div>
    </div>

    <div v-if="isChangingPassword">
        <div class="modal-overlay" @click.self="isChangingPassword = false">
            <div class="modal-content">
                <h3>修改密码</h3>
                <input type="password" v-model="oldPassword" placeholder="旧密码" class="modal-input" />
                <input type="password" v-model="newPassword" placeholder="新密码" class="modal-input" />
                <div class="modal-actions">
                    <button @click="changePassword" class="confirm-btn">确认修改</button>
                    <button @click="isChangingPassword = false" class="cancel-btn">取消</button>
                </div>
            </div>
        </div>
    </div>

    <!-- 上传歌曲弹窗 -->
    <div v-if="showUploadModal" class="modal-overlay" @click.self="showUploadModal = false">
        <div class="modal-content upload-modal">
            <h3>上传歌曲</h3>
            <div class="form-group">
                <label>歌曲标题</label>
                <input v-model="uploadForm.title" placeholder="请输入歌曲标题" class="modal-input" />
            </div>
            <div class="form-group">
                <label>音频文件</label>
                <input type="file" accept="audio/*" @change="handleFileChange" class="modal-input" />
            </div>
            <div class="form-group">
                <label>时长 (秒)</label>
                <input type="number" v-model="uploadForm.duration" placeholder="自动获取或手动输入" class="modal-input" />
            </div>
            <div class="form-group">
                <label>发布日期</label>
                <input type="date" v-model="uploadForm.release_date" class="modal-input" />
            </div>
             <div class="form-group">
                <label>专辑ID (可选)</label>
                <input v-model="uploadForm.album_id" placeholder="请输入专辑ID" class="modal-input" />
            </div>
             <div class="form-group">
                <label>封面URL (可选)</label>
                <input v-model="uploadForm.cover_url" placeholder="请输入封面图片URL" class="modal-input" />
            </div>
            <div class="modal-actions">
                <button @click="handleUploadSong" class="confirm-btn">确认上传</button>
                <button @click="showUploadModal = false" class="cancel-btn">取消</button>
            </div>
        </div>
    </div>

    <!-- 升级歌手弹窗 -->
    <div v-if="showUpgradeModal" class="modal-overlay" @click.self="showUpgradeModal = false">
        <div class="modal-content">
            <h3>申请成为歌手</h3>
            <p class="modal-tip">请输入您的艺名（默认为用户名）</p>
            <input v-model="artistName" :placeholder="username" class="modal-input" />
            <div class="modal-actions">
                <button @click="handleUpgrade" class="confirm-btn">确认申请</button>
                <button @click="showUpgradeModal = false" class="cancel-btn">取消</button>
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

    <!-- 创建专辑弹窗 -->
    <div v-if="showCreateAlbumModal" class="modal-overlay" @click.self="showCreateAlbumModal = false">
        <div class="modal-content">
            <h3>创建专辑</h3>
            <div class="form-group">
                <label>专辑名称</label>
                <input v-model="createAlbumForm.name" placeholder="请输入专辑名称" class="modal-input" />
            </div>
            <div class="form-group">
                <label>发布时间</label>
                <input type="date" v-model="createAlbumForm.release_time" class="modal-input" />
            </div>
            <div class="modal-actions">
                <button @click="handleCreateAlbum" class="confirm-btn">确认创建</button>
                <button @click="showCreateAlbumModal = false" class="cancel-btn">取消</button>
            </div>
        </div>
    </div>

    <!-- 管理歌曲专辑弹窗 -->
    <div v-if="showAddToAlbumModal" class="modal-overlay" @click.self="showAddToAlbumModal = false">
        <div class="modal-content">
            <h3>管理专辑</h3>
            <p>将歌曲添加到专辑 (或选择空移出专辑)</p>
            <div class="form-group">
                <label>选择专辑</label>
                <select v-model="selectedAlbumId" class="modal-input" style="width: 100%; padding: 8px;">
                    <option value="">(移出专辑)</option>
                    <option v-for="album in myAlbums" :key="album.album_id" :value="album.album_id">
                        {{ album.album_name }}
                    </option>
                </select>
            </div>
            <div class="modal-actions">
                <button @click="handleAddToAlbum" class="confirm-btn">确认保存</button>
                <button @click="showAddToAlbumModal = false" class="cancel-btn">取消</button>
            </div>
        </div>
    </div>

    <!-- 确认删除弹窗 -->
    <div v-if="showConfirmWindow" class="modal-overlay" @click.self="showConfirmWindow = false">
        <div class="modal-content">
            <h3>确认删除？</h3>
            <p v-if="pendingDelete && pendingDelete.msg" class="modal-tip">{{ pendingDelete.msg }}</p>
            <div class="modal-delete-actions">
                <button @click="confirmDelete" class="confirm-btn">确认</button>
                <button @click="showConfirmWindow = false" class="cancel-btn">取消</button>
            </div>
        </div>
    </div>
    <!-- 管理专辑内容弹窗 -->
    <div v-if="showManageAlbumContentModal" class="modal-overlay" @click.self="showManageAlbumContentModal = false">
        <div class="modal-content manage-album-modal">
            <h3>管理专辑内容: {{ currentManageAlbum?.album_name }}</h3>
            
            <div class="manage-section">
                <h4>专辑内歌曲</h4>
                <div v-if="currentAlbumSongs.length === 0" class="empty-tip-small">暂无歌曲</div>
                <ul class="song-list-small">
                    <li v-for="song in currentAlbumSongs" :key="song.song_id">
                        <span>{{ song.title }}</span>
                        <button @click="removeSongFromAlbum(song)" class="action-btn remove">移除</button>
                    </li>
                </ul>
            </div>

            <div class="divider"></div>

            <div class="manage-section">
                <h4>添加歌曲 (未归属专辑)</h4>
                <div v-if="availableSongs.length === 0" class="empty-tip-small">暂无可添加歌曲</div>
                <ul class="song-list-small">
                    <li v-for="song in availableSongs" :key="song.song_id">
                        <span>{{ song.title }}</span>
                        <button @click="addSongToAlbum(song)" class="action-btn add">添加</button>
                    </li>
                </ul>
            </div>

            <div class="modal-actions">
                <button @click="showManageAlbumContentModal = false" class="cancel-btn">关闭</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { showMessage } from '../../utils/message'
import { ref, onMounted, watch, computed } from 'vue'
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

const emit = defineEmits(['play', 'select-album', 'select-artist'])
import { upgradeToArtist, getUserInfo, updatePassword, updateUserName, getArtistProfile, updateArtistProfile } from '../../api/user'
import { uploadSong, getMySongs, deleteSong, updateSong } from '../../api/song'
import { createAlbum, getMyAlbums, deleteAlbum } from '../../api/album'

const currentContent = ref('favoriteSongsList')
const username = ref('')
const isArtist = ref(false)
const showUpgradeModal = ref(false)
const artistName = ref('')
const artistId = ref(null)
const isChangingPassword = ref(false)
const oldPassword = ref('')
const newPassword = ref('')

// Creator Center State
const creatorContent = ref('publishedSongs')
const mySongs = ref([])
const myAlbums = ref([])
const artistProfile = ref({
    name: '',
    region: '',
    bio: ''
})
const showCreateAlbumModal = ref(false)
const showAddToAlbumModal = ref(false)
const selectedSongId = ref(null)
const selectedAlbumId = ref('')
const createAlbumForm = ref({
    name: '',
    release_time: new Date().toISOString().split('T')[0],
})

// 个人信息
async function changeUserName() {
    if (!username.value.trim()) {
        showMessage('用户名不能为空', 'warning')
        return
    }
    try {
        await updateUserName(username.value)
        showMessage('用户名更新成功，请使用新用户名重新登录', 'success')
        
        // 更新成功后，强制退出登录，让用户用新名字重新登
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.href = '/login' 
    } catch (e) {
        showMessage(e.message || '更新失败', 'error')
    }
}

async function changePassword() {
    if (!newPassword.value.trim()) {
        showMessage('新密码不能为空', 'warning')
        return
    }
    if (!oldPassword.value.trim()) {
        showMessage('旧密码不能为空', 'warning')
        return
    }

    try {
        await updatePassword({ old_password: oldPassword.value, new_password: newPassword.value })
        showMessage('密码修改成功，请重新登录', 'success')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.href = '/login'
    } catch (e) {
        showMessage(e.message || '修改失败', 'error')
    }
}

// 上传歌曲相关
const showUploadModal = ref(false)
const uploadForm = ref({
    title: '',
    album_id: '',
    duration: '',
    release_date: new Date().toISOString().split('T')[0],
    file: null,
    cover_url: ''
})

function handleFileChange(event) {
    const file = event.target.files[0]
    if (file) {
        uploadForm.value.file = file
        // 尝试获取时长
        const audio = new Audio(URL.createObjectURL(file))
        audio.onloadedmetadata = () => {
            uploadForm.value.duration = Math.round(audio.duration)
        }
    }
}

async function handleUploadSong() {
    if (!uploadForm.value.title || !uploadForm.value.file || !uploadForm.value.duration || !uploadForm.value.release_date) {
        showMessage('请填写完整信息 (标题, 文件, 时长, 发布日期)', 'warning')
        return
    }
    
    const formData = new FormData()
    formData.append('title', uploadForm.value.title)
    if (uploadForm.value.album_id) formData.append('album_id', uploadForm.value.album_id)
    formData.append('duration', uploadForm.value.duration)
    formData.append('release_date', uploadForm.value.release_date)
    formData.append('audio_file', uploadForm.value.file)
    if (uploadForm.value.cover_url) formData.append('cover_url', uploadForm.value.cover_url)
    
    try {
        await uploadSong(formData)
        showMessage('上传成功！', 'success')
        showUploadModal.value = false
        // 重置表单
        uploadForm.value = {
            title: '',
            album_id: '',
            duration: '',
            release_date: new Date().toISOString().split('T')[0],
            file: null,
            cover_url: ''
        }
    } catch (e) {
        showMessage(e.message || '上传失败', 'error')
    }
}

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
            isArtist.value = user.role === 'artist'
            artistId.value = user.artist_id
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
        
        // 尝试获取最新的用户信息（以更新artist_id等）
        try {
            const userInfo = await getUserInfo()
            if (userInfo) {
                username.value = userInfo.username
                isArtist.value = userInfo.role === 'artist'
                artistId.value = userInfo.artist_id
                
                // 更新本地存储
                const localUser = JSON.parse(localStorage.getItem('user') || '{}')
                localUser.username = userInfo.username
                localUser.role = userInfo.role
                localUser.artist_id = userInfo.artist_id
                localStorage.setItem('user', JSON.stringify(localUser))
            }
        } catch (e) {
            console.warn('获取最新用户信息失败', e)
        }

    } catch (e) {
        console.error('加载数据失败', e)
    }
})

async function handleUpgrade() {
    if (!artistName.value.trim()) {
        showMessage('请输入歌手名称', 'warning')
        return
    }
    try {
        await upgradeToArtist(artistName.value)
        showMessage('升级成功！请重新登录以生效', 'success')
        // 更新本地存储的角色信息
        const userStr = localStorage.getItem('user')
        if (userStr) {
            const user = JSON.parse(userStr)
            user.role = 'artist'
            localStorage.setItem('user', JSON.stringify(user))
        }
        window.location.reload()
    } catch (e) {
        showMessage(e.message || '升级失败', 'error')
    }
}

// 添加收藏列表
async function addList() {
    if (!newListName.value.trim()) {
        showMessage('请输入列表名称', 'warning')
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
        showMessage(e.message || '添加失败', 'error')
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
        showMessage(e.message || '加载歌单歌曲失败', 'error')
    }
}

function backToCollections() {
    currentCollectionId.value = null
    currentCollectionListSongs.value = []
    currentCollectionListName.value = ''
}

function removeSongFromList(songId) {
    // TODO: 待实现移除功能
    showMessage('移除歌曲功能开发中...', 'info')
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
        } else if (type === 'myAlbum') {
            await deleteAlbum(id)
            loadCreatorData()
        } else if (type === 'mySong') {
            await deleteSong(id)
            loadCreatorData()
        }
        showConfirmWindow.value = false
        pendingDelete.value = null
    } catch (e) {
        showMessage(e.message || '删除失败', 'error')
    }
}

async function loadCreatorData() {
    try {
        const [songs, albums] = await Promise.all([getMySongs(), getMyAlbums()])
        mySongs.value = songs || []
        myAlbums.value = albums || []
    } catch (e) {
        console.error('加载创作者数据失败', e)
    }
}

async function loadArtistProfileData() {
    try {
        const data = await getArtistProfile()
        artistProfile.value = data
    } catch (e) {
        showMessage(e.message || '加载歌手信息失败', 'error')
    }
}

async function saveArtistProfile() {
    if (!artistProfile.value.name.trim()) {
        showMessage('歌手名称不能为空', 'warning')
        return
    }
    try {
        await updateArtistProfile(artistProfile.value)
        showMessage('保存成功', 'success')
    } catch (e) {
        showMessage(e.message || '保存失败', 'error')
    }
}

watch(currentContent, (newVal) => {
    if (newVal === 'creatorCenter') {
        loadCreatorData()
    }
})

watch(creatorContent, (newVal) => {
    if (newVal === 'artistProfile') {
        loadArtistProfileData()
    }
})

// 监听修改密码弹窗状态，关闭时清空输入框
watch(isChangingPassword, (val) => {
    if (!val) {
        oldPassword.value = ''
        newPassword.value = ''
    }
})

async function handleCreateAlbum() {
    if (!createAlbumForm.value.name || !createAlbumForm.value.release_time) {
        showMessage('请填写完整信息', 'warning')
        return
    }

    // 如果没有artistId，尝试重新获取用户信息
    if (!artistId.value) {
        try {
            const userInfo = await getUserInfo()
            if (userInfo && userInfo.artist_id) {
                artistId.value = userInfo.artist_id
                // 更新本地存储
                const localUser = JSON.parse(localStorage.getItem('user') || '{}')
                localUser.artist_id = userInfo.artist_id
                localStorage.setItem('user', JSON.stringify(localUser))
            }
        } catch (e) {
            console.warn('重试获取用户信息失败', e)
        }
    }

    if (!artistId.value) {
        showMessage('歌手信息校验失败。请确认您已登录且身份为歌手。若刚升级身份，请刷新页面重试。', 'error')
        return
    }

    try {
        await createAlbum({
            album_name: createAlbumForm.value.name,
            release_time: createAlbumForm.value.release_time,
            singer_id: artistId.value 
        })
        showMessage('创建专辑成功', 'success')
        showCreateAlbumModal.value = false
        createAlbumForm.value.name = ''
        loadCreatorData()
    } catch (e) {
        showMessage(e.message || '创建专辑失败', 'error')
    }
}

function handleDeleteSong(id) {
    pendingDelete.value = { type: 'mySong', id, msg: '确认删除此歌曲？' }
    showConfirmWindow.value = true
}

function handleDeleteAlbum(id) {
    pendingDelete.value = { 
        type: 'myAlbum', 
        id, 
        msg: '确认删除此专辑？(专辑内的歌曲将保留但移出专辑)' 
    }
    showConfirmWindow.value = true
}

function openAddToAlbum(song) {
    selectedSongId.value = song.song_id
    selectedAlbumId.value = song.album_id || ''
    showAddToAlbumModal.value = true
}

async function handleAddToAlbum() {
    try {
        await updateSong(selectedSongId.value, { album_id: selectedAlbumId.value || null })
        showMessage('更新成功', 'success')
        showAddToAlbumModal.value = false
        loadCreatorData()
    } catch (e) {
        showMessage(e.message || '更新失败', 'error')
    }
}

// Album Content Management
const showManageAlbumContentModal = ref(false)
const currentManageAlbum = ref(null)

const currentAlbumSongs = computed(() => {
    if (!currentManageAlbum.value) return []
    return mySongs.value.filter(s => s.album_id === currentManageAlbum.value.album_id)
})

const availableSongs = computed(() => {
    // Songs that are not in any album
    return mySongs.value.filter(s => !s.album_id)
})

function openManageAlbumContent(album) {
    currentManageAlbum.value = album
    showManageAlbumContentModal.value = true
}

async function addSongToAlbum(song) {
    if (!currentManageAlbum.value) return
    try {
        await updateSong(song.song_id, { album_id: currentManageAlbum.value.album_id })
        // Manually update local state for immediate UI feedback
        const target = mySongs.value.find(s => s.song_id === song.song_id)
        if (target) {
            target.album_id = currentManageAlbum.value.album_id
            target.album_title = currentManageAlbum.value.album_name
        }
    } catch (e) {
        showMessage(e.message || '添加失败', 'error')
    }
}

async function removeSongFromAlbum(song) {
    try {
        await updateSong(song.song_id, { album_id: null })
        // Manually update local state
        const target = mySongs.value.find(s => s.song_id === song.song_id)
        if (target) {
            target.album_id = null
            target.album_title = null
        }
    } catch (e) {
        showMessage(e.message || '移除失败', 'error')
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

.upgrade-section {
    margin-top: 40px;
    max-width: 500px;
}

.divider {
    height: 1px;
    background-color: #eee;
    margin-bottom: 20px;
}

.upgrade-desc {
    color: #666;
    font-size: 14px;
    margin: 10px 0 20px;
}

.upgrade-btn {
    padding: 10px 24px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    font-size: 16px;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 15px rgba(118, 75, 162, 0.3);
}

.upgrade-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(118, 75, 162, 0.4);
}

.modal-tip {
    font-size: 14px;
    color: #888;
    margin: -10px 0 10px;
    text-align: center;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.form-group label {
    font-size: 14px;
    font-weight: bold;
    color: #555;
}

.upload-modal {
    width: 500px; /* 稍微宽一点 */
    max-height: 90vh;
    overflow-y: auto;
}

.manage-album-modal {
    width: 500px;
    max-height: 80vh;
    overflow-y: auto;
}

.manage-section h4 {
    margin: 10px 0;
    color: #555;
    font-size: 14px;
    border-left: 3px solid #4caf50;
    padding-left: 8px;
}

.song-list-small {
    list-style: none;
    padding: 0;
    margin: 0;
    max-height: 150px;
    overflow-y: auto;
    border: 1px solid #eee;
    border-radius: 4px;
}

.song-list-small li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 10px;
    border-bottom: 1px solid #f9f9f9;
}

.song-list-small li:last-child {
    border-bottom: none;
}

.song-list-small li:hover {
    background-color: #f5f5f5;
}

.empty-tip-small {
    color: #999;
    font-size: 12px;
    padding: 10px;
    text-align: center;
    background: #f9f9f9;
    border-radius: 4px;
}

.action-btn {
    padding: 4px 8px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
}

.action-btn.add {
    background-color: #e3f2fd;
    color: #1976d2;
}

.action-btn.add:hover {
    background-color: #bbdefb;
}

.action-btn.remove {
    background-color: #ffebee;
    color: #d32f2f;
}

.action-btn.remove:hover {
    background-color: #ffcdd2;
}
</style>