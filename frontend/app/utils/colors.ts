import { colord, extend } from "colord";
import mixPlugin from "colord/plugins/mix";

extend([mixPlugin])

const gradientStops = [
  { sr: 1.5, color: "#4ebfff" },
  { sr: 2, color: "#4ef4db" },
  { sr: 2.75, color: "#8ffc50" },
  { sr: 3.3, color: "#f6ee5c" },
  { sr: 4, color: "#fcab63" },
  { sr: 5, color: "#fe676a" },
  { sr: 6, color: "#ff3c70" },
  { sr: 6.4, color: "#bb4ca0" },
  { sr: 7, color: "#6260db" },
  { sr: 7.99, color: "#18168e" },
  { sr: 8, color: "#000000" },
]

export function getColor(sr: number) {
  let lower: number = 0
  let higher: number = 0

  const dark = "#000000"
  const light = "#ffd700"
  const brightnessCutoff = 0.48

  for (let i = 0; i <= gradientStops.length - 1; i++) {
    if (sr > gradientStops[i].sr) {
      lower = i; higher = Math.min(i + 1, gradientStops.length - 1)
    }
  }

  if (lower === higher) {
    const color = colord(gradientStops[lower].color).toHex()
    const foreground = colord(color).brightness() >= brightnessCutoff ? dark : light
    return { color, foreground }
  }

  const range = gradientStops[higher].sr - gradientStops[lower].sr
  const lowerColorPercentage = (sr - gradientStops[lower].sr) * 1.0 / (range)
  const color = colord(gradientStops[higher].color).mix(gradientStops[lower].color, lowerColorPercentage).toHex()
  const foreground = colord(color).brightness() >= brightnessCutoff ? dark : light
  return { color, foreground }
}

