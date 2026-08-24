"use client"
import { useEffect, useState } from "react";

type Placeholder = {
  beatmap_id: number,
  beatmapset_id: number,
  title: string
}

export default function Page() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Placeholder[]>([])

  useEffect(() => {
    const timeout = setTimeout(async () => {
      if (query == '') {
        setResults([])
        return
      }
      const res = await fetch(`http://127.0.0.1:8000/api/search?q=${query}`)
      const data = await res.json()
      setResults(data)
      console.log(results)
    }, 400)

    return () => clearTimeout(timeout)
  }, [query])

  const handleChange = (e) => {
    setQuery(e.target.value)
  }
  return (
    <>
      <div>
        <h1>Beatmap Search</h1>
        <input type="text"

          placeholder="Search beatmap..."
          value={query}
          onChange={handleChange}
          className="w-[90%] px-4 py-3.5 text-base border border-[rgb(58,71,112)] bg-[rgb(38,44,66)] text-white rounded-xl mb-5 transition-all duration-200"
        />
        <div>
          {results.map(r => (
            <div key={r.beatmap_id}>
              <img src={`https://assets.ppy.sh/beatmaps/${r.beatmapset_id}/covers/cover.jpg`} alt="" />
              {r.title}
            </div>
          ))}
        </div>
      </div>
    </>
  )
}
