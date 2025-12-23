// 最小登录 API helper
export async function login({ username, password }) {
  const res = await fetch('/api/user/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ username, password }),
  })

  if (!res.ok) {
    let err = { detail: res.statusText }
    try { err = await res.json() } catch (e) {}
    throw new Error(err.detail || '登录失败')
  }

  return res.json()
}

export async function register({ username, password }) {
  const res = await fetch('/api/user/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username,
      password
    })
  })

  const data = await res.json()
  if (!res.ok || (typeof data.code !== 'undefined' && data.code !== 0)) {
    throw new Error(data.detail || data.message || '注册失败')
  }
  return data
}