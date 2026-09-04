import Link from "next/link";
import { Beatmaps } from "../types";
import Cover from "./BMSetCardParts/Cover";
import Image from "next/image";
import { getColor, getForegroundColor } from "../utils/colors";

interface Props {
  beatmaps: Beatmaps[]
}

export default function BeatmapsetCard({ beatmaps }: Props) {
  const bmsId = beatmaps[0].beatmapset_id
  const bmsTitle = beatmaps[0].title
  const bmsArtist = beatmaps[0].artist
  const bmsMapper = beatmaps[0].mapper
  return (
    <div className="group relative w-200 md:w-160 lg:w-240 h-fit flex flex-col items-center gap-8 rounded-t-md
    ">
      <Cover id={bmsId} title={bmsTitle} artist={bmsArtist} mapper={bmsMapper} />
      <div className="flex flex-col rounded-md
      absolute pt-60 left-0 w-full  pointer-events-none group-hover:pointer-events-auto  z-10
      opacity-0 max-h-0 overflow-hidden transition-all duration-300 group-hover:opacity-100 group-hover:max-h-fit
      hover:ring-1 hover:ring-blue-500/50 hover:ring-offset-2 hover:ring-offset-transparent hover:shadow-[0_0_15px_rgba(59,130,246,0.4)]
      ">
        {beatmaps.map(bm => (
          <Link key={bm.beatmap_id} href={`/beatmap/${bm.beatmap_id}`}>
            <div className="bg-(--color-background-secondary) py-2 px-3 transition-all duration-100 hover:bg-(--color-background-primary)">
              <span className="font-bold">
                <span style={{ backgroundColor: getColor(bm.star_rating).color, color: getColor(bm.star_rating).foreground }} className="p-1 px-3 rounded-xl">{bm.star_rating.toFixed(2)}</span> {bm.version}
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
