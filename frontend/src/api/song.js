import { getAuthHeaders, handleResponse } from './collection'

export async function uploadSong(formData) {
    const headers = getAuthHeaders()
    // 必须删除 Content-Type，让浏览器自动设置为 multipart/form-data 并带上 boundary
    delete headers['Content-Type']

    const res = await fetch('/api/song/my/create/', {
        method: 'POST',
        headers: headers,
        body: formData
    })

    return handleResponse(res, '上传失败')
}

export async function getMySongs() {
    const res = await fetch('/api/song/my/list/', {
        method: 'GET',
        headers: getAuthHeaders()
    })
    return handleResponse(res, '获取歌曲失败')
}

export async function updateSong(id, updateData) {
    const res = await fetch(`/api/song/my/${id}/`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(updateData)
    })
    return handleResponse(res, '更新歌曲失败')
}

export async function deleteSong(id) {
    const res = await fetch(`/api/song/my/${id}/delete/`, {
        method: 'DELETE',
        headers: getAuthHeaders()
    })
    return handleResponse(res, '删除歌曲失败')
}
