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
    <div className="w-200 md:w-160 lg:w-240 h-fit flex flex-row items-center gap-8 rounded-t-md
    transition-all duration-150 hover:ring-1 hover:ring-blue-500/50 hover:ring-offset-2 hover:ring-offset-transparent hover:shadow-[0_0_15px_rgba(59,130,246,0.4)]
    ">
      <Cover id={bmsId} title={bmsTitle} />
    </div>
  );
}
