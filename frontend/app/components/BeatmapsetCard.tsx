import Link from "next/link";
import { Beatmaps } from "../types";
import Cover from "./BMSetCardParts/Cover";
import Image from "next/image";

interface Props {
  beatmaps: Beatmaps[]
}

export default function BeatmapsetCard({ beatmaps }: Props) {
  const bmsId = beatmaps[0].beatmapset_id
  const bmsTitle = beatmaps[0].title
  return (
    <div className="group relative w-200 md:w-160 lg:w-240 h-fit flex flex-col items-center gap-8 rounded-t-md
    ">
      <Cover id={bmsId} title={bmsTitle} />
      <div className="flex flex-col rounded-md
      absolute pt-60 left-0 w-full  pointer-events-none group-hover:pointer-events-auto  z-10
      opacity-0 max-h-0 overflow-hidden transition-all duration-300 group-hover:opacity-100 group-hover:max-h-fit
      hover:ring-1 hover:ring-blue-500/50 hover:ring-offset-2 hover:ring-offset-transparent hover:shadow-[0_0_15px_rgba(59,130,246,0.4)]
      ">
        {beatmaps.map(bm => (
          <Link key={bm.beatmap_id} href={`/beatmap/${bm.beatmap_id}`}>
            <div className="bg-(--color-background-primary) py-2 px-3 transition-all duration-100 hover:bg-(--color-background-secondary)">
              {bm.version} {bm.star_rating.toFixed(2)}*
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
