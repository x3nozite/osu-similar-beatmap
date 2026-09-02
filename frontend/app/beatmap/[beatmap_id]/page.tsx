import HeroSection from "@/app/components/HeroSection";
import BeatmapCard from "@/app/components/BeatmapCard";
import { Beatmaps } from "@/app/types";


interface Props {
  params: Promise<{
    beatmap_id: number;
  }>
}

export default async function Page({ params }: Props) {
  const p = await params
  const beatmapId = p.beatmap_id
  const api_url = process.env.NEXT_PUBLIC_API_URL

  const res = await fetch(`${api_url}/api/beatmap/${beatmapId}`)
  const beatmap: Beatmaps = await res.json()

  const resSimilarBeatmap = await fetch(`${api_url}/api/beatmap/${beatmapId}/similar`)
  const similarBeatmap: Beatmaps[] = await resSimilarBeatmap.json()

  return (
    <div>
      <HeroSection
        beatmap={beatmap}
      />

      {similarBeatmap.map(bm => (
        <BeatmapCard beatmap={bm} key={bm.beatmap_id} />
      ))}
    </div>
  );
}
