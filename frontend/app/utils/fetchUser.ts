export type User = {
  osu_id: number;
  username: string
}

export async function FetchUser() {
  const api_url = process.env.NEXT_PUBLIC_API_URL
  let res = await fetch(`${api_url}/api/me`, { credentials: "include" })

  if (res.status === 401) {
    const refresh = await fetch(`${api_url}/api/token/refresh`, { method: "POST", credentials: "include" })
    if (refresh.ok) res = await fetch(`${api_url}/api/me`, { credentials: "include" })
  }

  if (res.ok) {
    const data: User = await res.json()
    return data
  } else {
    console.error(res)
    return null
  }

}
