<template>
    <li class="song-item">
        <div class="item-info">
            <div class="item-title">{{ song.title }}</div>
            <div class="item-sub">时长: {{ formatDuration(song.duration) }}</div>
            <div v-if="song.artist_name" class="item-sub">歌手: {{ song.artist_name }}</div>
            <div v-if="song.add_time" class="item-sub" style="font-size: 12px; color: #999;">收藏于: {{ formatDate(song.add_time) }}</div>
        </div>
        <div class="item-actions">
            <button class="action-btn btn-play" @click="$emit('play', song.audio_url)">▶ 播放</button>
            <button v-if="showRemove" class="remove-btn" @click="$emit('collect', song.song_id)">💔</button>
            <button v-else class="action-btn btn-collect" @click="$emit('collect', song.song_id)">❤ 收藏</button>
            <button class="action-btn btn-comment" @click="$emit('comment', song.song_id)">💬 评论</button>
        </div>
    </li>
</template>

<script setup>
import { defineComponent } from 'vue'

defineProps({
    song: {
        type: Object,
        required: true
    },
    showRemove: {
        type: Boolean,
        default: false
    }
})

defineEmits(['play', 'collect', 'comment'])

function formatDuration(seconds) {
    if (!seconds) return '0:00'
    const min = Math.floor(seconds / 60)
    const sec = seconds % 60
    return `${min}:${sec.toString().padStart(2, '0')}`
}

function formatDate(dateString) {
    if (!dateString) return '未知时间'
    let date = new Date(dateString)
    if (isNaN(date.getTime())) {
        date = new Date(dateString.replace(/-/g, '/'))
    }
    if (isNaN(date.getTime())) return '未知时间'
    return date.toLocaleString()
}
</script>

<style scoped>
.song-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    background: #f9f9f9;
    border-radius: 8px;
    transition: transform 0.2s, box-shadow 0.2s;
}

.song-item:hover {
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

.btn-collect {
    background-color: #fff0f0;
    color: #ef4444;
}
.btn-collect:hover {
    background-color: #ef4444;
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
</style>
