interface Props {
  params: Promise<{
    beatmap_id: string;
  }>
}

export default async function Page({ params }: Props) {
  const p = await params
  const beatmap_id = p.beatmap_id
  return (
    <div>
      hehe {beatmap_id}
    </div>
  );
}
