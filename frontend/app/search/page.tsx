"use client"
import Topbar from "../components/Topbar";
import { Beatmaps } from "../types";
import BeatmapCard from "../components/BeatmapCard";
import { useEffect, useState } from "react";


export default function Page() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Beatmaps[]>([])

  useEffect(() => {
    const timeout = setTimeout(async () => {
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
      <Topbar></Topbar>
      <div className="flex items-center justify-center">
        <div className="flex flex-col px-3 justify-center items-center w-200 bg-navy-bg-lighter">
          <input type="text"

            placeholder="Search beatmap..."
            value={query}
            onChange={handleChange}
            className="w-full px-4 py-3.5 text-base border border-[rgb(58,71,112)] bg-[rgb(38,44,66)] text-white rounded-xl mb-5 transition-all duration-200"
          />
          <div className="flex flex-col gap-4">
            {results.map(r => (
              <div key={r.beatmap_id}>
                <BeatmapCard beatmap={r} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}
