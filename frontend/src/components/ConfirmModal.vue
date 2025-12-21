<template>
    <div class="modal-overlay" @click.self="$emit('cancel')">
        <div class="modal-content">
            <h3>{{ title }}</h3>
            <p v-if="message" class="modal-tip">{{ message }}</p>
            <div class="modal-delete-actions">
                <button @click="$emit('confirm')" class="confirm-btn">确认</button>
                <button @click="$emit('cancel')" class="cancel-btn">取消</button>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    title: {
        type: String,
        default: '确认删除？'
    },
    message: {
        type: String,
        default: ''
    }
})

defineEmits(['confirm', 'cancel'])
</script>

<style scoped>
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

.modal-tip {
    font-size: 14px;
    color: #888;
    margin: -10px 0 10px;
    text-align: center;
}

.modal-delete-actions {
    display: flex;
    gap: 12px;
    justify-content: center;
}

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
</style>
