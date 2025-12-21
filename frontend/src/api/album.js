import { getAuthHeaders, handleResponse } from './collection'

export async function createAlbum(data) {
    const res = await fetch('/api/album/my/create/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data)
    })
    return handleResponse(res, '创建专辑失败')
}

export async function getMyAlbums() {
    const res = await fetch('/api/album/my/list/', {
        method: 'GET',
        headers: getAuthHeaders()
    })
    return handleResponse(res, '获取我的专辑失败')
}

export async function deleteAlbum(albumId) {
    const res = await fetch(`/api/album/my/${albumId}/delete/`, {
        method: 'DELETE',
        headers: getAuthHeaders()
    })
    // DELETE response might not be JSON if status is 204, but my backend returns JSON
    return handleResponse(res, '删除专辑失败')
}
