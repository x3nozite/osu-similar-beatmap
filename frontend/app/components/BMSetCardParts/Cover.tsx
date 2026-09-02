
import Image from "next/image";

interface Props {
  id: number;
  title: string;
}

export default function Cover({ id, title }: Props) {
  return (
    <div className="relative h-60 w-full overflow-hidden rounded-t-md">
      <Image
        src={`https://assets.ppy.sh/beatmaps/${id}/covers/card@2x.jpg`}
        alt=""
        fill
        sizes="(max-width: 768px) 100vw, 300px"
        className="object-cover brightness-50"
      />
      <div className="absolute inset-0 flex flex-row justify-center px-10">
        <h1 className="font-bold text-3xl">{title}</h1>
        <p></p>
      </div>

    </div>
  );
}
