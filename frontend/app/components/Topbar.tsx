import ButtonCustom from "./ButtonCustom";

export default function Topbar() {
  return (
    <div className="bg-topbar-bg top-0 inset-x-0 z-10 grid grid-cols-2 items-center px-6 py-3">
      <div>osu!similarity</div>
      <div className="flex justify-end">
        <ButtonCustom variant="osu"></ButtonCustom>
      </div>
    </div>
  );
}
