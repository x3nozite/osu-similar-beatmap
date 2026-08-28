export type User = {
  osu_id: number;
  username: string
}

export async function FetchUser() {
  const api_url = process.env.NEXT_PUBLIC_API_URL
  const res = await fetch(`${api_url}/api/me`, { credentials: 'include' })

  if (res.ok) {
    const data: User = await res.json()
    return data
  } else {
    console.error(res)
  }

  return null
}
