import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from util.queries import select_squad_players_count

st.set_page_config(layout="wide", page_title="Footstats", page_icon=":soccer:")

st.title(":bar_chart: Footstats - Football Statistics Dashboard :soccer:")

conn = st.connection("footstats", type="sql", autocommit=True)
df_squad_players_count = conn.query(select_squad_players_count)

st.write(
    """
    Welcome to our football stats dashboard! Here, you will find all the information you need to track and analyze your favorite team's performance. Let's take a look at how each section works:
    """
)

st.header(":athletic_shoe: Teams Statistics")

st.write(
    """
    - 🔍 **Players**: Search for the status of a specific player.
    - ⚽ **Goals**: Top scorers.
    - ⏱️ **Minutes Played**: Minutes played by each player for their team.
    """
)

st.header(":eyeglasses: Our teams")

num_rows = np.ceil(len(df_squad_players_count) / 3).astype(int)

rows = [st.columns(5) for _ in range(num_rows)]

for index, (team_name, players_count) in enumerate(
    zip(df_squad_players_count["Squad"], df_squad_players_count["Players"])
):
    row = index // 5
    col = index % 5

    current_col = rows[row][col]

    tile = current_col.container(height=120)
    tile.markdown(f":military_helmet: **{team_name}**")
    tile.write(f"Players: {players_count}")

st.header(":firefighter: Data quality")

st.write(
    """
    - 🔍 **Health Status**: Data ETL (Extract, Transform, Load) status.
    """
)

st.header("📊 Data Origin")
st.write(
    """
    - 🌐 **Source**: Brasileirão Serie A Stats from [https://fbref.com/en/comps/24/stats/Serie-A-Stats](https://fbref.com/en/comps/24/stats/Serie-A-Stats)
    """
)
