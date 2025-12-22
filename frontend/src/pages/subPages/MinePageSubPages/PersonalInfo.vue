<template>
    <div class="info-section">
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
            <button class="upgrade-btn" @click="openUpgradeModal">立即升级</button>
        </div>

        <!-- 修改密码弹窗 -->
        <div v-if="isChangingPassword" class="modal-overlay" @click.self="isChangingPassword = false">
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
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { showMessage } from '../../../utils/message'
import { upgradeToArtist, getUserInfo, updatePassword, updateUserName } from '../../../api/user'

const username = ref('')
const isArtist = ref(false)
const isChangingPassword = ref(false)
const oldPassword = ref('')
const newPassword = ref('')
const showUpgradeModal = ref(false)
const artistName = ref('')

onMounted(async () => {
    await loadUserInfo()
})

async function loadUserInfo() {
    try {
        const userStr = localStorage.getItem('user')
        if (userStr) {
            const user = JSON.parse(userStr)
            username.value = user.username || ''
            isArtist.value = user.role === 'artist'
        }
        
        // Fetch latest info
        const userInfo = await getUserInfo()
        if (userInfo) {
            username.value = userInfo.username
            isArtist.value = userInfo.role === 'artist'
            
            // Update local storage
            const localUser = JSON.parse(localStorage.getItem('user') || '{}')
            localUser.username = userInfo.username
            localUser.role = userInfo.role
            localUser.artist_id = userInfo.artist_id
            localStorage.setItem('user', JSON.stringify(localUser))
        }
    } catch (e) {
        console.warn('获取用户信息失败', e)
    }
}

async function changeUserName() {
    if (!username.value.trim()) {
        showMessage('用户名不能为空', 'warning')
        return
    }
    try {
        await updateUserName(username.value)
        showMessage('用户名更新成功，请使用新用户名重新登录', 'success')
        
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

function openUpgradeModal() {
    showUpgradeModal.value = true
    artistName.value = username.value
}

async function handleUpgrade() {
    if (!artistName.value.trim()) {
        showMessage('请输入歌手名称', 'warning')
        return
    }
    try {
        await upgradeToArtist(artistName.value)
        showMessage('升级成功！请重新登录以生效', 'success')
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

watch(isChangingPassword, (val) => {
    if (!val) {
        oldPassword.value = ''
        newPassword.value = ''
    }
})
</script>

<style scoped>
.info-section {
    margin-top: 30px;
    text-align: left;
    margin-left: 30px;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 12px;
    max-width: 500px;
    margin-top: 15px;
}

.label {
    font-weight: bold;
    color: #333;
    min-width: 60px;
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

.modal-tip {
    font-size: 14px;
    color: #888;
    margin: -10px 0 10px;
    text-align: center;
}
</style>
