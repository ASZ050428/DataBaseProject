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
