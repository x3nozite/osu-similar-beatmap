import HeroSection from "@/app/components/HeroSection";
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

  return (
    <div>
      <HeroSection
        beatmap={beatmap}
      />
    </div>
  );
}
