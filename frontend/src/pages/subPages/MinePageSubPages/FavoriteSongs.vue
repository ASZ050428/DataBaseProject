<template>
    <div class="fav-group">
        <!-- 列表模式 -->
        <div v-if="!currentCollectionId">
            <div class="group-header">
                <h3>收藏列表</h3>
                <button class="add-list" @click="showAddListModal = true">添加收藏列表</button>
            </div>
            <div v-if="loading" class="loading-tip">加载中...</div>
            <div v-else-if="favoriteSongsList.length === 0" class="empty-tip">暂无收藏歌曲</div>
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
            <div v-if="listLoading" class="loading-tip">加载中...</div>
            <div v-else-if="currentCollectionListSongs.length === 0" class="empty-tip">此歌单暂无歌曲</div>
            <ul v-else class="fav-list">
                <li v-for="song in currentCollectionListSongs" :key="song.id" class="fav-item">
                    <div class="fav-info" @click="$emit('play', song.audio_url)" style="cursor: pointer;" title="点击播放">
                        <div class="fav-title">▶ {{ song.title }}</div>
                    </div>
                    <div class="actions" style="display: flex; gap: 10px; align-items: center;">
                        <button @click="$emit('play', song.audio_url)" style="padding: 4px 8px; font-size: 12px; cursor: pointer;">▶ 播放</button>
                        <button class="remove-btn" @click="removeSongFromList(song.id)">💔</button>
                    </div>
                </li>
            </ul>
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
        <ConfirmModal 
            v-if="showConfirmWindow" 
            :message="pendingDelete?.msg || '确认删除此歌单？'"
            @confirm="confirmDelete" 
            @cancel="showConfirmWindow = false" 
        />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { showMessage } from '../../../utils/message'
import ConfirmModal from '../../../components/ConfirmModal.vue'
import { 
    getCollectionsList, 
    addCollection, 
    deleteCollection,
    getCollectionListSongs
} from '../../../api/collection'

const emit = defineEmits(['play'])

const favoriteSongsList = ref([])
const loading = ref(false)
const listLoading = ref(false)

// 详情页状态
const currentCollectionId = ref(null)
const currentCollectionListName = ref('')
const currentCollectionListSongs = ref([])

// 弹窗状态
const showAddListModal = ref(false)
const newListName = ref('')
const showConfirmWindow = ref(false)
const pendingDelete = ref(null)

onMounted(async () => {
    await loadCollections()
})

async function loadCollections() {
    loading.value = true
    try {
        const listsData = await getCollectionsList()
        favoriteSongsList.value = listsData || []
    } catch (e) {
        console.error('加载收藏列表失败', e)
    } finally {
        loading.value = false
    }
}

async function addList() {
    if (!newListName.value.trim()) {
        showMessage('请输入列表名称', 'warning')
        return
    }
    
    try {
        const newList = await addCollection(newListName.value)
        favoriteSongsList.value.unshift(newList)
        newListName.value = ''
        showAddListModal.value = false
    } catch (e) {
        showMessage(e.message || '添加失败', 'error')
    }
}

async function showCollectionList(list) {
    try {
        currentCollectionListName.value = list.title
        currentCollectionId.value = list.id
        listLoading.value = true
        const songs = await getCollectionListSongs(list.id)
        currentCollectionListSongs.value = songs || []
    } catch (e) {
        showMessage(e.message || '加载歌单歌曲失败', 'error')
    } finally {
        listLoading.value = false
    }
}

function backToCollections() {
    currentCollectionId.value = null
    currentCollectionListSongs.value = []
    currentCollectionListName.value = ''
}

function removeSongFromList(songId) {
    showMessage('移除歌曲功能开发中...', 'info')
}

function removeList(id) {
    pendingDelete.value = { id }
    showConfirmWindow.value = true
}

async function confirmDelete() {
    if (!pendingDelete.value) return
    
    const { id } = pendingDelete.value
    try {
        await deleteCollection(id)
        favoriteSongsList.value = favoriteSongsList.value.filter(item => item.id !== id)
        showConfirmWindow.value = false
        pendingDelete.value = null
    } catch (e) {
        showMessage(e.message || '删除失败', 'error')
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

.empty-tip, .loading-tip {
    color: #999;
    font-style: italic;
    padding: 20px 0;
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
</style>
