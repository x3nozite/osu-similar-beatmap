interface Props {
  query: string;
  handleChange: (e) => void;
}

export default function InputBox({ query, handleChange }: Props) {
  return (
    <input type="text"

      placeholder="Search beatmap..."
      value={query}
      onChange={handleChange}
      className="w-full px-4 py-3.5 text-base border border-[rgb(58,71,112)] bg-[rgb(38,44,66)] text-white rounded-xl transition-all duration-200"
    />
  );
}
