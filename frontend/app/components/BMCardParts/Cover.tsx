import Image from "next/image";

interface Props {
  id: number;
}

export default function Cover({ id }: Props) {
  return (
    <div className="relative h-full w-[30%] rounded-md overflow-hidden">
      <Image
        src={`https://assets.ppy.sh/beatmaps/${id}/covers/card@2x.jpg`}
        alt=""
        fill
        sizes="(max-width: 768px) 100vw, 300px"
        className="object-cover"
      />

    </div>
  );
}
