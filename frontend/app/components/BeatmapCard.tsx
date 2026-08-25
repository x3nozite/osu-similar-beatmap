import Cover from "./BMCardParts/Cover";
import { Beatmaps } from "../types";

interface Props {
  beatmap: Beatmaps
}

export default function BeatmapCard({ beatmap }: Props) {
  return (
    <div className="bg-[#3a4770] w-240 h-60 shadow-[0_4px_8px_rgba(0,0,0,0.3)] rounded-lg flex flex-row items-center gap-8">
      <Cover id={beatmap.beatmapset_id}></Cover>
      <p>{beatmap.title} : {beatmap.version}</p>
    </div>
  );
}
