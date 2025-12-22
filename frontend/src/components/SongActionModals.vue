<template>
    <div>
        <!-- 收藏弹窗 -->
        <div v-if="collectVisible" class="modal-overlay" @click="$emit('close')">
            <div class="modal-content" @click.stop>
                <h3>选择收藏歌单</h3>
                <div v-if="collectionsLoading" class="loading-tip">加载中...</div>
                <div v-else-if="collections.length === 0" class="empty-list">
                    暂无歌单，请先去"我的"页面创建
                </div>
                <ul v-else class="collection-list">
                    <li v-for="list in collections" :key="list.id" @click="$emit('add-to-collection', list.id)">
                        {{ list.title }}
                    </li>
                </ul>
                <button class="close-btn" @click="$emit('close')">取消</button>
            </div>
        </div>

        <!-- 评论弹窗 -->
        <div v-if="commentVisible" class="modal-overlay" @click="$emit('close')">
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
                    <textarea 
                        :value="commentContent" 
                        @input="$emit('update:commentContent', $event.target.value)"
                        placeholder="写下你的评论..." 
                        rows="3"
                    ></textarea>
                    <div class="modal-footer">
                        <button class="close-modal-btn" @click="$emit('close')">关闭</button>
                        <button class="submit-btn" @click="$emit('submit-comment')" :disabled="!commentContent.trim()">发表评论</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    collectVisible: Boolean,
    commentVisible: Boolean,
    collections: Array,
    collectionsLoading: Boolean,
    comments: Array,
    commentsLoading: Boolean,
    commentContent: String
})

defineEmits(['close', 'add-to-collection', 'submit-comment', 'update:commentContent'])

function formatDate(dateStr) {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleString()
}
</script>

<style scoped>
/* 弹窗通用样式 */
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

.empty-tip {
    color: #999;
    font-style: italic;
    margin-left: 25px;
    padding: 10px 0;
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
