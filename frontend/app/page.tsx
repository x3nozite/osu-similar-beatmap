"use client"
import Image from "next/image";
import Topbar from "./components/Topbar";
import { useEffect, useState } from "react";
import { Beatmaps } from "./types";

export default function Page() {
  const api_url = process.env.NEXT_PUBLIC_API_URL
  const [background, setBackground] = useState("")
  useEffect(() => {
    async function getRandomBeatmap() {
      const res = await fetch(`${api_url}/api/beatmap/random`)
      console.log(res)
      const data: Beatmaps = await res.json()
      console.log(data)

      setBackground(`https://assets.ppy.sh/beatmaps/${data.beatmapset_id}/covers/card@2x.jpg`)
    }

    getRandomBeatmap()
  }, [])

  return (
    <div>
      <Topbar />
      <div className="relative w-10 h-10">
        {background && (
          <Image src={background} alt="" fill className="object-cover" />
        )}
      </div>
    </div>
  );
}
