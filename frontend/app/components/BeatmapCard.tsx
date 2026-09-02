import Cover from "./BMCardParts/Cover";
import CardDetails from "./BMCardParts/CardDetails";
import Link from "next/link";
import { Beatmaps } from "../types";

interface Props {
  beatmap: Beatmaps
}

export default function BeatmapCard({ beatmap }: Props) {
  const osu_link = "https://osu.ppy.sh"
  return (
    <Link href={`${osu_link}/beatmapsets/${beatmap.beatmapset_id}`} target="_blank" rel="noopener noreferrer">
      <div className="bg-[#3a4770] w-full md:w-160 lg:w-240 h-60 shadow-[0_4px_8px_rgba(0,0,0,0.3)] rounded-lg flex flex-row items-center gap-8 transition-all duration-150 hover:ring-2 hover:ring-blue-500/50 hover:ring-offset-2 hover:ring-offset-transparent hover:shadow-[0_0_15px_rgba(59,130,246,0.4)]">
        <Cover id={beatmap.beatmapset_id}></Cover>
        <div className="h-full py-8">
          <CardDetails
            beatmap={beatmap}
          />
        </div>
      </div>
    </Link>
  );
}
