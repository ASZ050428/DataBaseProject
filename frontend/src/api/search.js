export async function searchSong(songName) {
    const res = await fetch(`/api/song/?search=${encodeURIComponent(songName)}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '搜索歌曲失败')
    }
    return data.data
}

export async function searchAlbum(albumName) {
    const res = await fetch(`/api/album/?search=${encodeURIComponent(albumName)}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '搜索专辑失败')
    }
    return data.data
}

export async function searchArtist(artistName) {
    const res = await fetch(`/api/artist/?search=${encodeURIComponent(artistName)}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    })

    const data = await res.json()
    if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
        throw new Error(data.message || '搜索歌手失败')
    }
    return data.data
}