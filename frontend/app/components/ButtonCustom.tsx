const variants = {
  primary: "bg-violet-500  text-white hover:bg-violet-400",
  secondary: "border border-violet-400 text-violet-300 hover:bg-violet-950",
  osu: "bg-osu-pink text-white hover:bg-osu-pink-darker",
} satisfies Record<string, string>

const sizes = {
  sm: "px-2 py-1 text-sm",
  md: "px-4 py-2 text-md",
  lg: "px-6 py-3 text-lg"
} satisfies Record<string, string>

interface Props {
  variant?: keyof typeof variants,
  size?: keyof typeof sizes,
  className?: string
}

export default function ButtonCustom({ variant = "primary", size = "md", className = "" }: Props) {
  return (
    <button className={`text-base rounded-md   transition duration-200 ${variants[variant]} ${sizes[size]} ${className}`}>
      Login with osu!
    </button>
  );
}
