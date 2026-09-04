import { Beatmaps } from "@/app/types";
import { getColor } from "@/app/utils/colors";

interface Props {
  beatmap: Beatmaps
}

export default function CardDetails({ beatmap }: Props) {
  return (
    <div className="flex flex-col gap-2 w-full min-w-0">
      <h1 className="whitespace-nowrap overflow-hidden text-ellipsis w-150 md:w-75 lg:w-150 block box-border text-3xl font-bold" title={beatmap.title}>
        {beatmap.title}
      </h1>
      <div className="flex flex-col gap-1">
        <p>{beatmap.artist}</p>
        <p>[{beatmap.version}]</p>
      </div>
      <div className="text-sm">
        <p>
          Mapped by <span className="font-bold">{beatmap.mapper}</span> | Star Rating:
          <span style={{ backgroundColor: getColor(beatmap.star_rating).color, color: getColor(beatmap.star_rating).foreground }} className="p-1 px-3 rounded-xl ml-1 font-bold">{beatmap.star_rating.toFixed(2)}</span>

          {/* <span className="font-bold">{beatmap.star_rating.toFixed(2)}*</span> */}
        </p>
      </div>
    </div>
  );
}
