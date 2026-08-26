import Link from "next/link";
import ButtonCustom from "./ButtonCustom";

export default function Topbar() {
  return (
    <div className="bg-topbar-bg top-0 inset-x-0 z-10 grid grid-cols-2 items-center px-6 py-3">
      <div>
        <Link href="/">osu!similarity</Link>
      </div>
      <div className="flex justify-end">
        <ButtonCustom variant="osu" text="Sign up with osu!" onClick={() => { }} />
      </div>
    </div>
  );
}
