import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from util.queries import select_minutes_all

st.set_page_config(layout="wide", page_title="Minutes Played", page_icon=":hourglass_flowing_sand:")

st.title(":hourglass_flowing_sand: Minutes Played")

conn = st.connection("footstats", type="sql", autocommit=True)
df_minutes = conn.query(select_minutes_all)

unique_squads = np.sort(df_minutes["Squad"].unique())
selected_squad = st.sidebar.selectbox("Select a Squad:", unique_squads)

st.header(selected_squad)

df_minutes_filtered = df_minutes[df_minutes["Squad"] == selected_squad]
df_minutes_filtered = df_minutes_filtered.sort_values(
    by=["Minutes_Played", "Starts"], ascending=[True, True]
)
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

max_minutes_index = df_minutes_filtered["Minutes_Played"].idxmax()
max_minutes_player = df_minutes_filtered.loc[max_minutes_index, "Player"]
max_minutes_played = df_minutes_filtered.loc[max_minutes_index, "Minutes_Played"]
average_minutes = df_minutes_filtered["Minutes_Played"].mean()
players_started_games = df_minutes_filtered[df_minutes_filtered["Starts"] > 0].shape[0]
players_above_average_minutes = (df_minutes_filtered["Minutes_Played"] > average_minutes).sum()
total_players = df_minutes_filtered.shape[0]
max_minutes_value = int(df_minutes_filtered["Starts"].max()) * 90
if max_minutes_value < max_minutes_played:
    max_minutes_value = max_minutes_played

metrics = col1.container()

correlation = df_minutes_filtered["Starts"].corr(df_minutes_filtered["Minutes_Played"])
average_minutes_per_start = (
    df_minutes_filtered["Minutes_Played"].sum() / df_minutes_filtered["Starts"].sum()
)
max_ratio_player = df_minutes_filtered.loc[
    (df_minutes_filtered["Minutes_Played"] / df_minutes_filtered["Starts"]).idxmax(), "Player"
]
players_above_average_minutes = (df_minutes_filtered["Minutes_Played"] > average_minutes).sum()

metrics.subheader(f"**Player with most minutes**:")
metrics.markdown(max_minutes_player)
fig_max_minutes_player = px.pie(
    names=["Minutes", "Total"],
    values=[
        max_minutes_played,
        max_minutes_value - max_minutes_played,
    ],
    hole=0.5,
    color_discrete_sequence=px.colors.sequential.Inferno,
)
fig_max_minutes_player.update_layout(
    annotations=[
        dict(text=f"{max_minutes_played:.2f}", x=0.5, y=0.5, font_size=16, showarrow=False)
    ],
    width=300,
    height=300,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
    ),
    margin=dict(l=0, r=100, t=0, b=0),
)
metrics.plotly_chart(fig_max_minutes_player)

metrics.subheader(f"**Average minutes**")
fig_average_minutes = px.pie(
    names=["Average", "Total"],
    values=[
        average_minutes,
        max_minutes_value - average_minutes,
    ],
    hole=0.5,
    color_discrete_sequence=px.colors.sequential.Inferno,
)
fig_average_minutes.update_layout(
    annotations=[dict(text=f"{average_minutes:.2f}", x=0.5, y=0.5, font_size=16, showarrow=False)],
    width=300,
    height=300,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
    ),
    margin=dict(l=0, r=100, t=0, b=0),
)
metrics.plotly_chart(fig_average_minutes)

col2.subheader("Visualizations")

fig_bar_minutes_played = px.bar(
    df_minutes_filtered,
    x="Minutes_Played",
    y="Player",
    color="Starts",
    orientation="h",
    title=f"Minutes Played and Starts",
    labels={"Minutes_Played": "Minutes Played", "Player": "Player", "Starts": "Starts"},
    color_continuous_scale=px.colors.sequential.Inferno,
)

fig_bar_minutes_played.update_layout(
    barmode="group", xaxis_title="Minutes Played", yaxis_title="Player"
)
col2.plotly_chart(fig_bar_minutes_played)

fig_scatter_minutes = px.scatter(
    df_minutes_filtered,
    x="Starts",
    y="Minutes_Played",
    color="Player",
    title=f"Relationship between Starts and Minutes Played",
    labels={"Starts": "Starts", "Minutes_Played": "Minutes Played"},
)
col2.plotly_chart(fig_scatter_minutes)

col3.subheader(f"Minutes played")
col3.data_editor(
    df_minutes_filtered[["Player", "Minutes_Played"]],
    column_config={
        "Minutes_Played": st.column_config.ProgressColumn(
            "Minutes Played",
            help=f"Total minutes played by the player considering maximum as {max_minutes_value}",
            format="%f",
            min_value=0,
            max_value=int(max_minutes_value),
        ),
    },
    hide_index=True,
)

col3.subheader(f"Statistics")

col3.data_editor(
    df_minutes_filtered[["Minutes_Played", "Starts"]].describe(),
    column_config={
        "Minutes_Played": st.column_config.NumberColumn(
            "Minutes Played",
            format="%.2f",
        ),
        "Starts": st.column_config.NumberColumn(
            "Starts",
            format="%.2f",
        ),
    },
    hide_index=False,
)
