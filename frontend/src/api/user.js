import { getAuthHeaders, handleResponse } from './collection'

export async function upgradeToArtist(artistName) {
    const res = await fetch('/api/auth/upgrade-artist/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ name: artistName })
    })

    return handleResponse(res, '升级失败')
}

export async function getUserInfo() {
    const res = await fetch('/api/auth/me/', {
        method: 'GET',
        headers: getAuthHeaders()
    })
    
    return handleResponse(res, '获取用户信息失败')
}
