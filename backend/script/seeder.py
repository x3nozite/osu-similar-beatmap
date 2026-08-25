from datasets import load_dataset
import json
from huggingface_hub import login
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

load_dotenv()
hf_token = os.getenv("HF_TOKEN")
login(token=hf_token)

conn = psycopg2.connect(
    host="localhost",
    dbname="beatmap_similarity",
    user="postgres",
    password=""
)
batch = []
BATCH_SIZE = 500


shards = [f"compressed/data-{i:06d}.tar" for i in range(18, 20)]
# 1,20
ds = load_dataset(
    "project-riz/osu-beatmaps",
    "compressed",
    data_files={"train": shards},
    streaming=True,
)
stream = ds["train"].remove_columns(["opus"])


def insert_batch(conn, rows):
    cols = list(rows[0].keys())
    values = []
    for r in rows:
        row_val = []
        for c in cols:
            row_val.append(r[c])
        values.append(row_val)

    query = f"""
        insert into beatmaps({','.join(cols)})
        values %s
        on conflict (beatmap_id) do nothing
    """

    with conn.cursor() as cur:
        execute_values(cur, query, values)
    conn.commit()


i = 0
for sample in stream:
    data = sample["json"]
    print("new audio.. ", i)
    beatmaps = data.get("beatmaps", [])

    for beatmap in beatmaps:
        if (beatmap.get("mode") != 0):
            continue

        # Inspect the raw .osu chart file content
        osu_content = beatmap.get("content", "")

        circle_count = beatmap.get("count_normal")
        slider_count = beatmap.get("count_slider")
        spinner_count = beatmap.get("count_spinner")
        drain_length = beatmap.get("hit_length")

        density = (circle_count + slider_count + spinner_count) / drain_length
        tap_ratio = circle_count / \
            (circle_count + slider_count + spinner_count)

        row = {
            "beatmap_id": beatmap.get("beatmap_id"),
            "beatmapset_id": beatmap.get("beatmapset_id"),
            "title": beatmap.get('title'),
            "artist": beatmap.get("artist"),
            "mapper": beatmap.get("creator"),
            "version": beatmap.get("version"),
            "mode": beatmap.get("mode"),
            "bpm": beatmap.get("bpm"),
            "star_rating": beatmap.get("difficultyrating"),
            "diff_aim": beatmap.get("diff_aim"),
            "diff_speed": beatmap.get("diff_speed"),
            "ar": beatmap.get("diff_approach"),
            "cs": beatmap.get("diff_size"),
            "od": beatmap.get("diff_overall"),
            "hp": beatmap.get("diff_drain"),
            "drain_time": beatmap.get("hit_length"),
            "circle_count": circle_count,
            "slider_count": slider_count,
            "spinner_count": spinner_count,
            "density": density,
            "tap_ratio": tap_ratio,
        }
        batch.append(row)
        if (len(batch) >= BATCH_SIZE):
            insert_batch(conn, batch)
            batch = []

        i += 1
        # title_line = next(
        #     (line for line in osu_content.splitlines() if line.startswith("Title:")), None)

        # print("\n".join(osu_content.splitlines()[:15]))

if batch:
    insert_batch(conn, batch)
print("done")
