"use client"
import { Beatmaps } from "../types";
import BeatmapCard from "../components/BeatmapCard";
import { SlidersHorizontal } from "lucide-react";
import InputBox from "../components/InputBox";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { useEffect, useState } from "react";

export default function Page() {
  const api_url = process.env.NEXT_PUBLIC_API_URL
  const [results, setResults] = useState<Beatmaps[]>([])
  const [showFilters, setShowFilters] = useState(false)
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const query = searchParams.get('q') || ''
  const [currentQuery, setCurrentQuery] = useState(query)

  useEffect(() => {
    const timeout = setTimeout(async () => {
      const res = await fetch(`${api_url}/api/search?q=${query}`)
      const data = await res.json()
      setResults(data)
      console.log(results)
    }, 100)

    return () => clearTimeout(timeout)
  }, [query])

  useEffect(() => {
    const timeout = setTimeout(async () => {
      const newQuery = currentQuery
      const params = new URLSearchParams(searchParams)

      if (newQuery) params.set('q', newQuery)
      else params.delete('q')

      router.push(`${pathname}?${params.toString()}`)
    }, 400)

    return () => clearTimeout(timeout)
  }, [currentQuery])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCurrentQuery(e.target.value)
  }

  const toggleFilter = () => {
    setShowFilters(prev => !prev)
  }

  return (
    <>
      <div className="flex items-center justify-center">
        <div className="flex flex-col px-8 py-4 justify-center items-center w-auto bg-background-secondary gap-8">
          <div className="w-full flex flex-row gap-4 items-center">
            <InputBox
              query={currentQuery}
              handleChange={handleChange}
            />
            <button onClick={toggleFilter}>
              <SlidersHorizontal />
            </button>
          </div>
          {showFilters && (
            <div>filters</div>
          )}
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
