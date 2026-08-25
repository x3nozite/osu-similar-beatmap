import { Beatmaps } from "@/app/types";

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
          Mapped by <span className="font-bold">{beatmap.mapper}</span> | Star Rating: {beatmap.star_rating.toFixed(2)}*
        </p>
      </div>
    </div>
  );
}
