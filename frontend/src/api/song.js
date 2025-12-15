import { getAuthHeaders } from './collection'

export async function uploadSong(formData) {
    const headers = getAuthHeaders()
    // 必须删除 Content-Type，让浏览器自动设置为 multipart/form-data 并带上 boundary
    delete headers['Content-Type']

    const res = await fetch('/api/song/my/create/', {
        method: 'POST',
        headers: headers,
        body: formData
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '上传失败')
    }
    return data
}
