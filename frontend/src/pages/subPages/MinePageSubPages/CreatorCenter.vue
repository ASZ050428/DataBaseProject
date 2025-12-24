<template>
    <div class="fav-group">
        <div class="group-header">
            <h3>创作者中心</h3>
            <div class="creator-actions">
                <button class="add-list" @click="showUploadModal = true">发布歌曲</button>
                <button class="add-list" @click="showCreateAlbumModal = true">发布专辑</button>
            </div>
        </div>

        <div class="sub-nav">
            <span class="nav-item" :class="{ active: creatorContent === 'publishedSongs' }"
                @click="creatorContent = 'publishedSongs'">已发布歌曲</span>
            <span class="nav-item" :class="{ active: creatorContent === 'publishedAlbums' }"
                @click="creatorContent = 'publishedAlbums'">已发布专辑</span>
            <span class="nav-item" :class="{ active: creatorContent === 'artistProfile' }"
                @click="creatorContent = 'artistProfile'">歌手信息</span>
        </div>

        <div v-if="creatorContent === 'publishedSongs'">
            <div v-if="mySongs.length === 0" class="empty-tip">暂无发布歌曲</div>
            <ul v-else class="fav-list">
                <li v-for="song in mySongs" :key="song.song_id" class="fav-item">
                    <div class="fav-info">
                        <div class="fav-title">{{ song.title }}</div>
                        <div class="fav-sub">{{ song.album_title ? `专辑: ${song.album_title}` : '未归属专辑' }}</div>
                    </div>
                    <div class="item-actions">
                        <button @click="emit('play', song.audio_url)" class="small-btn">▶ 播放</button>
                        <button class="remove-btn" @click="handleDeleteSong(song.song_id)">🗑️</button>
                    </div>
                </li>
            </ul>
        </div>

        <div v-if="creatorContent === 'publishedAlbums'">
            <div v-if="myAlbums.length === 0" class="empty-tip">暂无发布专辑</div>
            <ul v-else class="fav-list">
                <li v-for="album in myAlbums" :key="album.album_id" class="fav-item">
                    <div class="fav-info clickable" @click="emit('select-album', album.album_id)" title="点击查看专辑详情">
                        <div class="fav-title">{{ album.album_name }}</div>
                        <div class="fav-sub">发布于: {{ album.release_time }}</div>
                    </div>
                    <div class="item-actions">
                        <button @click="openManageAlbumContent(album)" class="small-btn">管理内容</button>
                        <button class="remove-btn" @click="handleDeleteAlbum(album.album_id)">🗑️</button>
                    </div>
                </li>
            </ul>
        </div>

        <div v-if="creatorContent === 'artistProfile'" class="info-section">
            <div class="info-item">
                <span class="label">歌手名称</span>
                <input type="text" v-model="artistProfile.name" placeholder="请输入歌手名称" />
            </div>
            <div class="info-item">
                <span class="label">地区</span>
                <input type="text" v-model="artistProfile.region" placeholder="请输入地区" />
            </div>
            <div class="info-item align-start">
                <span class="label top-align">简介</span>
                <textarea v-model="artistProfile.bio" placeholder="请输入简介" class="bio-textarea"></textarea>
            </div>
            <div class="info-item">
                <button @click="saveArtistProfile">保存修改</button>
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
                <div class="modal-actions">
                    <button @click="handleUploadSong" class="confirm-btn">确认上传</button>
                    <button @click="showUploadModal = false" class="cancel-btn">取消</button>
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

        <!-- 确认删除弹窗 -->
        <ConfirmModal v-if="showConfirmWindow" :message="pendingDelete?.msg" @confirm="confirmDelete"
            @cancel="showConfirmWindow = false" />

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
    </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { showMessage } from '../../../utils/message'
import { getUserInfo, getArtistProfile, updateArtistProfile } from '../../../api/user'
import { uploadSong, getMySongs, deleteSong, updateSong } from '../../../api/song'
import { createAlbum, getMyAlbums, deleteAlbum } from '../../../api/album'
import ConfirmModal from '../../../components/ConfirmModal.vue'

const emit = defineEmits(['play', 'select-album'])

const creatorContent = ref('publishedSongs')
const mySongs = ref([])
const myAlbums = ref([])
const artistProfile = ref({
    name: '',
    region: '',
    bio: ''
})
const artistId = ref(null)

// Modals
const showUploadModal = ref(false)
const showCreateAlbumModal = ref(false)
const showManageAlbumContentModal = ref(false)
const showConfirmWindow = ref(false)
const pendingDelete = ref(null)

// Forms & Selections
const uploadForm = ref({
    title: '',
    album_id: '',
    duration: '',
    release_date: new Date().toISOString().split('T')[0],
    file: null,
    cover_url: ''
})
const createAlbumForm = ref({
    name: '',
    release_time: new Date().toISOString().split('T')[0],
})
const currentManageAlbum = ref(null)

onMounted(async () => {
    await loadUserInfo()
    await loadCreatorData()
})

async function loadUserInfo() {
    try {
        const userStr = localStorage.getItem('user')
        if (userStr) {
            const user = JSON.parse(userStr)
            artistId.value = user.artist_id
        }
        // Fetch latest to be sure
        const userInfo = await getUserInfo()
        if (userInfo) {
            artistId.value = userInfo.artist_id
        }
    } catch (e) {
        console.warn('获取用户信息失败', e)
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

watch(creatorContent, (newVal) => {
    if (newVal === 'artistProfile') {
        loadArtistProfileData()
    }
})

// Upload Song
function handleFileChange(event) {
    const file = event.target.files[0]
    if (file) {
        uploadForm.value.file = file
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

    try {
        await uploadSong(formData)
        showMessage('上传成功！', 'success')
        showUploadModal.value = false
        uploadForm.value = {
            title: '',
            album_id: '',
            duration: '',
            release_date: new Date().toISOString().split('T')[0],
        }
        loadCreatorData()
    } catch (e) {
        showMessage(e.message || '上传失败', 'error')
    }
}

// Create Album
async function handleCreateAlbum() {
    if (!createAlbumForm.value.name || !createAlbumForm.value.release_time) {
        showMessage('请填写完整信息', 'warning')
        return
    }

    if (!artistId.value) {
        showMessage('歌手信息校验失败。请确认您已登录且身份为歌手。', 'error')
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

// Delete Handlers
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

async function confirmDelete() {
    if (!pendingDelete.value) return

    const { type, id } = pendingDelete.value
    try {
        if (type === 'myAlbum') {
            await deleteAlbum(id)
        } else if (type === 'mySong') {
            await deleteSong(id)
        }
        await loadCreatorData()
        showConfirmWindow.value = false
        pendingDelete.value = null
    } catch (e) {
        showMessage(e.message || '删除失败', 'error')
    }
}

// Manage Album Content
const currentAlbumSongs = computed(() => {
    if (!currentManageAlbum.value) return []
    return mySongs.value.filter(s => s.album_id === currentManageAlbum.value.album_id)
})

const availableSongs = computed(() => {
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
.fav-group h3 {
    font-size: 18px;
    color: #555;
    margin: 0;
}

.group-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    border-bottom: 2px solid #f0f0f0;
    padding-bottom: 10px;
}

.creator-actions {
    display: flex;
    gap: 10px;
}

.add-list {
    padding: 6px 14px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.add-list:hover {
    background-color: #45a049;
}

.sub-nav {
    margin-bottom: 20px;
    display: flex;
    gap: 20px;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.nav-item {
    cursor: pointer;
    padding: 5px 10px;
    color: #666;
    border-bottom: 2px solid transparent;
}

.nav-item.active {
    font-weight: bold;
    color: #4caf50;
    border-bottom: 2px solid #4caf50;
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
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    background: #fff;
}

.fav-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.clickable {
    cursor: pointer;
}

.fav-title {
    font-weight: bold;
    font-size: 16px;
    color: #333;
}

.fav-sub {
    font-size: 12px;
    color: #888;
}

.item-actions {
    display: flex;
    gap: 10px;
    align-items: center;
}

.small-btn {
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
    background-color: #ebf2ff;
    color: #2563eb;
}

.small-btn:hover {
    background-color: #2563eb;
    color: white;
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
}

.empty-tip {
    color: #999;
    font-style: italic;
    padding: 20px 0;
}

.info-section {
    margin: 0;
    text-align: left;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 12px;
    max-width: 500px;
    margin-top: 15px;
}

.info-item.align-start {
    align-items: flex-start;
}

.label {
    font-weight: bold;
    color: #333;
    min-width: 60px;
}

.label.top-align {
    margin-top: 8px;
}

.info-item input {
    flex: 1;
    padding: 8px 12px;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
}

.info-item input:focus {
    border-color: #2563eb;
}

.bio-textarea {
    flex: 1;
    padding: 8px 12px;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    font-size: 16px;
    outline: none;
    min-height: 100px;
    resize: vertical;
    font-family: inherit;
}

.info-item button {
    padding: 6px 14px;
    background-color: #3cc0ef;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s;
    white-space: nowrap;
}

.info-item button:hover {
    background-color: #3298eb;
}

/* Modal Styles */
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

.full-width-select {
    width: 100%;
    padding: 8px;
}

.modal-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
}

.modal-actions button {
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
    width: 500px;
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
