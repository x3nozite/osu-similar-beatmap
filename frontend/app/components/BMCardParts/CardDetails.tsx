import { Beatmaps } from "@/app/types";

interface Props {
  beatmap: Beatmaps
}

export default function CardDetails({ beatmap }: Props) {
  return (
    <div className="flex flex-col gap-2 w-full">
      <h1 className="whitespace-nowrap overflow-hidden text-ellipsis max-w-full block box-border text-3xl font-bold">
        {beatmap.title}
      </h1>
      <div className="flex flex-col gap-1">
        <p>{beatmap.artist}</p>
        <p>[{beatmap.version}]</p>
      </div>
      <div className="text-sm">
        <p>
          Mapped by {beatmap.mapper} | Star Rating: {beatmap.star_rating}*
        </p>
      </div>
    </div>
  );
}
