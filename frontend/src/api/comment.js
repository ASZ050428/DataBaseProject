import { getAuthHeaders, handleResponse } from './collection'

// 获取歌曲评论列表
export async function getSongComments(songId) {
    const res = await fetch(`/api/comment/by-song/${songId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    return handleResponse(res, '获取评论失败')
}

// 发表评论
export async function postComment(songId, content) {
    const res = await fetch(`/api/comment/my/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ song_id: songId, content })
    })
    return handleResponse(res, '发表评论失败')
}

// 删除评论
export async function deleteComment(commentId) {
    const res = await fetch(`/api/comment/my/${commentId}/`, {
        method: 'DELETE',
        headers: getAuthHeaders()
    })
    return handleResponse(res, '删除评论失败')
}