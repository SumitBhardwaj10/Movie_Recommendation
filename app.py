import streamlit as st
from typing import List
import joblib
import numpy as np
import pandas as pd

st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎥", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 10% 10%, #0f172a 0%, #0b1220 40%, #070d18 100%);
        color: #e5e7eb;
    }
    .app-title {
        font-size: 48px; line-height:1.1; font-weight:800; letter-spacing:-0.5px;
        background: linear-gradient(90deg, #93c5fd, #c084fc, #fb7185);
        -webkit-background-clip: text; background-clip: text; color: transparent; margin-bottom: 6px;
    }
    .app-sub {
        color: #94a3b8; margin-bottom: 24px; font-size: 16px;
    }
    .glass {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(148,163,184,0.15);
        box-shadow: 0 8px 30px rgba(0,0,0,0.35);
        border-radius: 18px; padding: 20px; backdrop-filter: blur(8px);
    }
    .pill {
        display:inline-block; padding:6px 12px; border-radius:999px; border:1px solid rgba(148,163,184,0.25);
        background: rgba(148,163,184,0.08); font-size:12px; color:#cbd5e1; margin-right:8px;
    }
    .btn-primary button {
        border-radius: 999px !important; font-weight:700 !important; padding: 10px 18px !important;
        box-shadow: 0 8px 20px rgba(59,130,246,0.25) !important;
    }
    .movie-card {border-radius: 18px; padding: 16px; border:1px solid rgba(148,163,184,0.15);
                 background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
                 height: 180px; display:flex; flex-direction:column; justify-content:space-between;}
    .movie-rank {font-size:12px; color:#94a3b8;}
    .movie-title {font-size:16px; font-weight:700; color:#e5e7eb;}
    .chip {font-size:11px; padding:4px 8px; border-radius:999px; border:1px solid rgba(148,163,184,0.25); color:#cbd5e1;}
    .footer-note {color:#64748b; font-size:12px; margin-top:8px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-title">Movie Recommender</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-sub">Pick a movie and get five similar gems. Built for speed, simplicity, and style ✨</div>',
    unsafe_allow_html=True,
)

with st.container():
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.subheader("🏹 Select a movie")

        movies=joblib.load("Files/movies.pkl")
        movies = pd.DataFrame(movies)
        movie_titles=list(movies["title"].values)

        default_opt = movie_titles[0] if movie_titles else None
        selected_title = st.selectbox("Movie title", options=movie_titles, index=0 if default_opt else None, placeholder="Type to search…")

        c1, c2, c3 = st.columns([0.22, 0.22, 0.56])
        with c1:
            st.metric(label="Movies", value=f"{len(movie_titles):,}")
        with c2:
            st.metric(label="Recs per pick", value="5")
        with c3:
            st.caption("Tip: start typing to quickly filter titles.")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.write(
            "This app recommends five similar movies using your precomputed similarity. Load your catalog on the left, then click Recommend."
        )
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("\n")

cta_col1, cta_col2, _ = st.columns([0.2, 0.2, 0.6])
with cta_col1:
    recommend_clicked = st.button("🔎 Recommend", use_container_width=True, type="primary")
with cta_col2:
    st.button("🔄 Clear", use_container_width=True)

st.markdown("\n")

results_container = st.container()

if recommend_clicked and selected_title:
    similarity_matrix=joblib.load("Files/similarity.pkl")
    index = movies[movies["title"] == selected_title].index
    top_5 = similarity_matrix[index[0]]
    values = movies.iloc[top_5]["title"].values
    recommended = movies.iloc[top_5]["title"].values

    with results_container:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown(f"### Top 5 for **{selected_title}**")
        cols = st.columns(5)
        for i in range(5):
            with cols[i % 5]:
                try:
                    title = recommended[i]
                except Exception:
                    title = "(your result here)"
                st.markdown(
                    f"""
                    <div class='movie-card'>
                        <div class='movie-rank'>#{i+1}</div>
                        <div class='movie-title'>{title}</div>
                        <div style='display:flex; gap:8px; align-items:center;'>
                            <span class='chip'>Similar</span>
                            <span class='chip'>Top Pick</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)

elif recommend_clicked and not selected_title:
    st.warning("Please select a movie first.")

st.markdown('<div class="footer-note">Analysis with Sumit ❤️</div>', unsafe_allow_html=True)
