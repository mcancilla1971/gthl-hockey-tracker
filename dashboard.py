import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="GTHL U12 AA Tracker",
    page_icon="🏒",
    layout="wide"
)

st.title("🏒 GTHL U12 AA Hockey Tracker")
st.caption("2026–27 Season | East & West Divisions")

csv_file = Path(__file__).parent / "gthl_u12_aa_standings.csv"

if not csv_file.exists():
    st.error("Standings CSV not found.")
    st.stop()

df = pd.read_csv(csv_file)

for col in ["GP", "PTS", "WIN%", "GFA", "GAA"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Goal Differential"] = df["GFA"] - df["GAA"]

region = st.selectbox(
    "Select Division",
    ["All", "West", "East"]
)

if region != "All":
    df = df[df["Region"] == region]

st.subheader("League Standings")

st.dataframe(
    df.sort_values("PTS", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.subheader("Compare Teams")

teams = st.multiselect(
    "Select teams",
    options=sorted(df["Team"].dropna().unique()),
    default=[
        t for t in ["The Attack", "Toronto Eagles", "West Mall Lightning"]
        if t in df["Team"].values
    ]
)

if teams:
    comparison = df[df["Team"].isin(teams)]
    st.bar_chart(
        comparison.set_index("Team")[
            ["GFA", "GAA"]
        ]
    )
    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )
