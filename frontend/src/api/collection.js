// 获取本地存储的 Token
function getAuthHeaders() {
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

// 1. 获取我的收藏歌单列表
export async function getCollectionsList() {
    const res = await fetch('/api/collection/my/lists/', {
        method: 'GET',
        headers: getAuthHeaders(),
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '获取收藏列表失败')
    }
    return data.data // 返回实际的列表数据
}

// 2. 创建新的收藏歌单
export async function addCollection(name) {
    const res = await fetch('/api/collection/my/lists/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ name })
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '创建歌单失败')
    }
    return data.data // 返回新创建的歌单信息 {id, title}
}

// 3. 删除收藏歌单
export async function deleteCollection(listId) {
    const res = await fetch(`/api/collection/my/lists/${listId}/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '删除歌单失败')
    }
    return true
}

// 4. 获取我的收藏专辑
export async function getFavoriteAlbums() {
    const res = await fetch('/api/collection/my/albums/', {
        method: 'GET',
        headers: getAuthHeaders(),
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '获取收藏专辑失败')
    }
    return data.data
}

// 5. 取消收藏专辑
export async function removeFavoriteAlbum(albumId) {
    const res = await fetch(`/api/collection/my/albums/${albumId}/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '取消收藏专辑失败')
    }
    return true
}

// 6. 获取我关注的歌手
export async function getFavoriteArtists() {
    const res = await fetch('/api/collection/my/artists/', {
        method: 'GET',
        headers: getAuthHeaders(),
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '获取关注歌手失败')
    }
    return data.data
}

// 7. 取消关注歌手
export async function removeFavoriteArtist(artistId) {
    const res = await fetch(`/api/collection/my/artists/${artistId}/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '取消关注歌手失败')
    }
    return true
}