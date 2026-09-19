# osu! Beatmap Similarity Engine

A recommendation engine for osu! standard beatmaps. Instead of relying on tags or text search, it converts each beatmap's playstyle attributes into a feature vector and finds maps that are mathematically similar.

Live demo: https://osu-similar-beatmap-seven.vercel.app/

## Features
- Similarity search: pick a beatmap and get back others that play similarly, based on playstyle attributes rather than tags or text matching.
- Tag-aware scoring: factors in community tags (e.g. "jumps," "streams," "tech"), weighted by each tag's share of a beatmapset's total votes so niche maps with few votes aren't penalized against heavily-voted popular ones.
- Search: find beatmaps by title, artist, mapper, or difficulty name, with results grouped by beatmapset.

Each beatmap is represented by two feature vectors: a normalized numeric vector, and a tag vector. The two scores are blended into one weighted result.

A handful of joke/troll beatmaps exist with absurd BPM or star rating values, which would badly distort plain min-max normalization for everyone else. Columns prone to this use percentile-clipped normalization; columns that turned out to be naturally well-behaved (density, tap ratio, AR, CS) use plain min-max.

## Tech stack

- **Frontend**: Next.js (TypeScript), Tailwind CSS
- **Backend**: FastAPI, SQLModel
- **Database**: PostgreSQL (Neon)

## Data

Beatmap data is sourced from public HuggingFace datasets (`project-riz/osu-beatmaps` for metadata, `project-riz/osu-beatmap-tags` for community tags).
