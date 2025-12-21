import { getAuthHeaders } from './collection'

export async function upgradeToArtist(artistName) {
    const res = await fetch('/api/auth/upgrade-artist/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ name: artistName })
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '升级失败')
    }
    return data
}

export async function getUserInfo() {
    const res = await fetch('/api/auth/me/', {
        method: 'GET',
        headers: getAuthHeaders()
    })
    
    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        // 静默失败或抛出异常，视情况而定
        throw new Error(data.message || '获取用户信息失败')
    }
    return data.data
}

export async function updateUserName(newUsername) {
    const res = await fetch('/api/auth/me/', {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({ username: newUsername })
    })
    
    let data;
    try {
        data = await res.json()
    } catch (e) {
        throw new Error(`服务器响应异常 (${res.status})`)
    }

    if (!res.ok) {
        throw new Error(data.message || `请求失败 (${res.status})`)
    }

    if (typeof data.code !== 'undefined' && data.code !== 0) {
        throw new Error(data.message || '更新用户名失败')
    }
    return data
}

export async function updatePassword(data) {
    const res = await fetch('/api/auth/change-password/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data)
    })
    
    let resData;
    try {
        resData = await res.json()
    } catch (e) {
        throw new Error(`服务器响应异常 (${res.status})`)
    }

    if (!res.ok) {
        throw new Error(resData.message || `请求失败 (${res.status})`)
    }

    if (typeof resData.code !== 'undefined' && resData.code !== 0) {
        throw new Error(resData.message || '修改密码失败')
    }
    return resData
}
