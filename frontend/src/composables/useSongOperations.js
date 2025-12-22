import { ref } from 'vue'
import { getCollectionsList, addSongToCollection } from '../api/collection'
import { getSongComments, postComment } from '../api/comment'
import { showMessage } from '../utils/message'

export function useSongOperations() {
    // 状态
    const collectModalVisible = ref(false)
    const commentModalVisible = ref(false)
    const currentSongId = ref(null)
    
    // 收藏相关
    const userCollections = ref([])
    const collectionsLoading = ref(false)
    
    // 评论相关
    const comments = ref([])
    const commentsLoading = ref(false)
    const commentContent = ref('')

    // 打开收藏弹窗
    async function openCollectModal(songId) {
        currentSongId.value = songId
        collectModalVisible.value = true
        collectionsLoading.value = true
        try {
            const list = await getCollectionsList()
            userCollections.value = Array.isArray(list) ? list : []
        } catch (e) {
            showMessage(e.message || '获取歌单失败', 'error')
        } finally {
            collectionsLoading.value = false
        }
    }

    // 确认收藏
    async function addToCollection(listId) {
        if (!currentSongId.value) return
        try {
            await addSongToCollection(listId, currentSongId.value)
            showMessage('收藏成功！', 'success')
            collectModalVisible.value = false
        } catch (e) {
            showMessage(e.message || '收藏失败', 'error')
        }
    }

    // 打开评论弹窗
    async function openCommentModal(songId) {
        currentSongId.value = songId
        commentModalVisible.value = true
        commentContent.value = ''
        await loadComments(songId)
    }

    // 加载评论
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

    // 发表评论
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

    // 关闭所有弹窗
    function closeModals() {
        collectModalVisible.value = false
        commentModalVisible.value = false
        currentSongId.value = null
    }

    return {
        // 状态
        collectModalVisible,
        commentModalVisible,
        currentSongId,
        userCollections,
        collectionsLoading,
        comments,
        commentsLoading,
        commentContent,
        
        // 方法
        openCollectModal,
        addToCollection,
        openCommentModal,
        submitComment,
        closeModals
    }
}
