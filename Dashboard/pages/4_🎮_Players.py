import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from util.queries import select_squads, select_player, select_player_history

st.set_page_config(layout="wide", page_title="Players", page_icon=":video_game:")
st.title(":video_game: Players")

conn = st.connection("footstats", type="sql", autocommit=True)
df_squads = conn.query(select_squads)

unique_squads = np.sort(df_squads["Squad"])
selected_squad = st.sidebar.selectbox("Select a Squad:", unique_squads)
player_name = st.sidebar.text_input("Enter a player name:")
df_player = None
df_player_history = None

if df_player is None and player_name == "":
    st.warning("Please enter a player name.")

if st.sidebar.button("Search") and player_name != "":
    df_player = conn.query(
        select_player,
        params={"squad": selected_squad, "player": f"%{player_name}%"},
    )
    df_player_history = conn.query(
        select_player_history,
        params={"squad": selected_squad, "player": f"%{player_name}%"},
    )

    if df_player.empty:
        st.warning("No data found.")

if df_player is not None and not df_player.empty:
    st.header(f":soccer: {selected_squad}")
    for _, row in df_player.iterrows():
        st.subheader(f":bust_in_silhouette: {row['Player']} ({row['Position']})")
        col1, col2 = st.columns(2)
        col1.write(f":earth_americas: **Nation**: {row['Nation']}")
        col1.write(f":birthday: **Birth Year**: {row['Birth_Year']}")
        col1.write(f":video_game: **Matches Played**: {row['Matches_Played']}")
        col1.write(f":stopwatch: **Minutes Played**: {row['Minutes_Played']}")
        col1.write(f":goal_net: **Goals**: {row['Goals']}")
        col1.write(f":handshake: **Assists**: {row['Assists']}")

        # Adicionando métricas para cartões amarelos e vermelhos
        col2.metric(":large_yellow_square: Yellow Cards", row.get("Yellow_Cards", 0))
        col2.metric(":large_red_square: Red Cards", row.get("Red_Cards", 0))

        if df_player_history is not None and not df_player_history.empty:
            df_player_history_filtered = df_player_history[
                (df_player_history["Player"] == row["Player"])
                & (df_player_history["Squad"] == selected_squad)
            ]
            fig_goals = px.line(
                df_player_history_filtered,
                x="Created_Date",
                y="Goals",
                title="Goals by match",
                labels={"Created_Date": "Date"},
            )
            fig_goals.update_yaxes(rangemode="tozero", dtick=1)
            col1.plotly_chart(fig_goals)
            fig_minutes = px.line(
                df_player_history_filtered,
                x="Created_Date",
                y="Minutes_Played",
                title="Goals by match",
                labels={"Created_Date": "Date", "Minutes_Played": "Minutes Played"},
            )
            fig_minutes.update_yaxes(rangemode="tozero")
            col1.plotly_chart(fig_minutes)
