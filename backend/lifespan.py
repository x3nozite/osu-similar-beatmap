from contextlib import asynccontextmanager
from fastapi import FastAPI
from beatmaps.models import Beatmaps
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from database import engine
from sqlmodel import Session, select


@asynccontextmanager
async def lifespan(app: FastAPI):
    with Session(engine) as session:
        beatmaps = session.exec(select(Beatmaps)).all()
        app.state.numeric_matrix = np.array([
            [bm.bpm_norm, bm.diff_aim_norm, bm.diff_speed_norm,
                bm.ar_norm, bm.cs_norm, bm.density_norm, bm.tap_ratio_norm]
            for bm in beatmaps
        ])

        app.state.beatmap_id_index = {
            bm.beatmap_id: i for i, bm in enumerate(beatmaps)}

        cursor = engine.raw_connection().cursor()
        cursor.execute("""
        select beatmapset_id, string_agg(tag_name, ' ') as tags
        from beatmapset_tags
        group by beatmapset_id
        """)

        rows = cursor.fetchall()
        beatmapset_ids = [r[0] for r in rows]
        tag_documents = [r[1] for r in rows]

        vectorizer = CountVectorizer(tokenizer=lambda x: x.split())
        X_sparse = vectorizer.fit_transform(tag_documents)

        vocab = vectorizer.vocabulary_
        id_to_index = {bms_id: i for i, bms_id in enumerate(beatmapset_ids)}

        app.state.tag_matrix = X_sparse
        app.state.tag_vocab = vocab
        app.state.beatmapset_id_index = id_to_index
        app.state.beatmap_to_beatmapset = {
            bm.beatmap_id: bm.beatmapset_id for bm in beatmaps}

    yield
