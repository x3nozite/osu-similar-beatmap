"use client"
import Image from "next/image";
import Topbar from "./components/Topbar";
import { useEffect, useState } from "react";
import InputBox from "./components/InputBox";
import ButtonCustom from "./components/ButtonCustom";
import { useRouter } from "next/navigation";
import { Beatmaps } from "./types";

export default function Page() {
  const api_url = process.env.NEXT_PUBLIC_API_URL
  const [background, setBackground] = useState("")
  const [query, setQuery] = useState('')
  const router = useRouter()

  useEffect(() => {
    async function getRandomBeatmap() {
      const res = await fetch(`${api_url}/api/beatmap/random`)
      const data: Beatmaps = await res.json()
      console.log(data)

      setBackground(`https://assets.ppy.sh/beatmaps/${data.beatmapset_id}/covers/fullsize.jpg`)
    }

    getRandomBeatmap()
  }, [])

  const handleChange = (e) => {
    setQuery(e.target.value)
  }

  const search = () => {
    router.push(`search/?q=${query}`)
  }

  return (
    <div>
      <Topbar />
      <div className="relative w-full h-240">
        {background && (
          <>
            <Image src={background} alt="" fill className="object-cover" />
            <div className="bg-gradient-to-r from-[var(--color-background-primary)] from-30% to-transparent w-full h-full absolute inset-0"></div>
            <div className="absolute inset-0 flex flex-col justify-center px-12 gap-8">
              <h1 className="text-4xl font-bold text-white">Welcome to osu!similarity</h1>
              <div className="flex flex-row gap-8 w-1/2 md:w-150 lg:w-1/2">
                <InputBox
                  query={query}
                  handleChange={handleChange}
                />
                <ButtonCustom text="Search" onClick={search} />
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
