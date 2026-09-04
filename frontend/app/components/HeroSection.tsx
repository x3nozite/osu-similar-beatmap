import Image from "next/image";
import { Beatmaps } from "../types";

interface Props {
  beatmap: Beatmaps;
}

export default function HeroSection({ beatmap }: Props) {
  const beatmapsetId = beatmap.beatmapset_id
  const beatmapId = beatmap.beatmap_id
  return (
    <div className="p-4 relative h-100">
      <Image
        src={`https://assets.ppy.sh/beatmaps/${beatmapsetId}/covers/fullsize.jpg`}
        alt=''
        fill
        className="object-cover brightness-50" />
      <div className="absolute inset-0 flex flex-col justify-center px-10">
        <h1 className="font-bold text-4xl">{beatmap.title}</h1>
        <p className="text-lg">[{beatmap.version}] {beatmap.star_rating.toFixed(2)}*</p>
      </div>
    </div>
  );
}
