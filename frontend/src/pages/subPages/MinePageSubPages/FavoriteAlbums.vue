<template>
    <div class="fav-group">
        <div class="group-header">
            <h3>专辑</h3>
        </div>
        <div v-if="loading" class="loading-tip">加载中...</div>
        <div v-else-if="favoriteAlbums.length === 0" class="empty-tip">暂无收藏专辑</div>
        <ul v-else class="fav-list">
            <li v-for="album in favoriteAlbums" :key="album.id" class="fav-item" @click="$emit('select-album', album.id)">
                <div class="fav-info" style="cursor: pointer">
                    <div class="fav-title">{{ album.title }}</div>
                </div>
                <button class="remove-btn" @click="removeAlbum(album.id)">💔</button>
            </li>
        </ul>

        <ConfirmModal 
            v-if="showConfirmWindow" 
            :message="'确认移除此专辑？'"
            @confirm="confirmDelete" 
            @cancel="showConfirmWindow = false" 
        />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { showMessage } from '../../../utils/message'
import ConfirmModal from '../../../components/ConfirmModal.vue'
import { getFavoriteAlbums, removeFavoriteAlbum } from '../../../api/collection'

const emit = defineEmits(['select-album'])

const favoriteAlbums = ref([])
const loading = ref(false)
const showConfirmWindow = ref(false)
const pendingDeleteId = ref(null)

onMounted(async () => {
    await loadAlbums()
})

async function loadAlbums() {
    loading.value = true
    try {
        const albumsData = await getFavoriteAlbums()
        favoriteAlbums.value = albumsData || []
    } catch (e) {
        console.error('加载收藏专辑失败', e)
    } finally {
        loading.value = false
    }
}

function removeAlbum(id) {
    pendingDeleteId.value = id
    showConfirmWindow.value = true
}

async function confirmDelete() {
    if (!pendingDeleteId.value) return
    
    try {
        await removeFavoriteAlbum(pendingDeleteId.value)
        favoriteAlbums.value = favoriteAlbums.value.filter(item => item.id !== pendingDeleteId.value)
        showConfirmWindow.value = false
        pendingDeleteId.value = null
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
</style>
