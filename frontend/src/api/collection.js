// 获取本地存储的 Token
export function getAuthHeaders() {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const token = user.access
    const headers = {
        'Content-Type': 'application/json',
    }
    if (token) {
        headers['Authorization'] = `Bearer ${token}`
    }
    return headers
}

export async function handleResponse(res, defaultErrorMsg) {
    if (res.status === 401) {
        localStorage.removeItem('user')
        window.location.href = '/login'
        throw new Error('登录已过期，请重新登录')
    }
    
    let data;
    const text = await res.text();
    try {
        data = text ? JSON.parse(text) : {};
    } catch (e) {
        console.error('Response parse error:', e, 'Text:', text);
        throw new Error(defaultErrorMsg + ': 服务器响应格式错误');
    }

    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || defaultErrorMsg)
    }
    return data.data
}

// 1. 获取我的收藏歌单列表
export async function getCollectionsList() {
    const res = await fetch('/api/collection/my/lists/', {
        method: 'GET',
        headers: getAuthHeaders(),
    })
    return handleResponse(res, '获取收藏列表失败')
}

// 2. 创建新的收藏歌单
export async function addCollection(name) {
    const res = await fetch('/api/collection/my/lists/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ name })
    })
    return handleResponse(res, '创建歌单失败')
}

// 3. 删除收藏歌单
export async function deleteCollection(listId) {
    const res = await fetch(`/api/collection/my/lists/${listId}/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    })
    // DELETE usually returns 204 or empty body, but this API seems to return JSON based on previous code
    // Previous code: const data = await res.json(); ... return true
    // Let's check handleResponse. It expects JSON.
    // If backend returns 204, res.json() will fail.
    // Let's check the backend view MyCollectionListDeleteView.
    // It returns api_response(message='删除成功', data=None), which is JSON.
    // So handleResponse is fine, but it returns data.data which is None.
    // The original code returned true.
    
    await handleResponse(res, '删除歌单失败')
    return true
}

// 4. 获取我的收藏专辑
export async function getFavoriteAlbums() {
    const res = await fetch('/api/collection/my/albums/', {
        method: 'GET',
        headers: getAuthHeaders(),
    })
    return handleResponse(res, '获取收藏专辑失败')
}

// 5. 取消收藏专辑
export async function removeFavoriteAlbum(albumId) {
    const res = await fetch(`/api/collection/my/albums/${albumId}/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    })
    await handleResponse(res, '取消收藏专辑失败')
    return true
}

export async function addFavoriteAlbum(albumId) {
    const res = await fetch('/api/collection/my/albums/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ album_id: albumId })
    })
    return handleResponse(res, '收藏专辑失败')
}

// 6. 获取我关注的歌手
export async function getFavoriteArtists() {
    const res = await fetch('/api/collection/my/artists/', {
        method: 'GET',
        headers: getAuthHeaders(),
    })
    return handleResponse(res, '获取关注歌手失败')
}

// 7. 取消关注歌手
export async function removeFavoriteArtist(artistId) {
    const res = await fetch(`/api/collection/my/artists/${artistId}/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    })
    await handleResponse(res, '取消关注歌手失败')
    return true
}

export async function addFavoriteArtist(artistId) {
    const res = await fetch('/api/collection/my/artists/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ artist_id: artistId })
    })
    return handleResponse(res, '关注歌手失败')
}

export async function getCollectionListSongs(listId) {
    const res = await fetch(`/api/collection/my/lists/${listId}/songs/`, {
        method: 'GET',
        headers: getAuthHeaders(),
    })
    return handleResponse(res, '获取歌单歌曲失败')
}

export async function addSongToCollection(listId, songId) {
    const res = await fetch(`/api/collection/my/lists/${listId}/songs/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ song_id: songId })
    })
    return handleResponse(res, '添加歌曲失败')
}

export async function removeSongFromCollection(listId, songId) {
    const res = await fetch(`/api/collection/my/lists/${listId}/songs/${songId}/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    })
    await handleResponse(res, '移除歌曲失败')
    return true
}