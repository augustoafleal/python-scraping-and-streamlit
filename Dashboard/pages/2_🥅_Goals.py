import streamlit as st
import plotly.express as px
import pandas as pd
from util.queries import select_goals

st.set_page_config(layout="wide", page_title="Goals", page_icon=":goal_net:")

st.title(":goal_net: Goals")

conn = st.connection("footstats", type="sql", autocommit=True)
stats = conn.query(select_goals)
df_stats = pd.DataFrame(stats)

st.subheader("Goals Scoring")

df_stats["Player_Squad"] = df_stats["Player"] + " - " + df_stats["Squad"]
df_stats_goals_players = (
    df_stats[["Goals", "Player_Squad"]]
    .sort_values(by=["Goals", "Player_Squad"], ascending=False)
    .iloc[:10]
)

fig_bar_goals_players = px.bar(
    df_stats_goals_players,
    x="Player_Squad",
    y="Goals",
    title="Goal Scores by Players",
    color="Player_Squad",
)
fig_bar_goals_players.update_layout(xaxis_title="Player - Squad")
st.plotly_chart(fig_bar_goals_players, use_container_width=True)

df_stats_goals_teams = (
    df_stats[["Goals", "Squad"]]
    .groupby(by="Squad", as_index=False)
    .sum()
    .sort_values(by=["Goals", "Squad"], ascending=False)
    .iloc[:10]
)
fig_bar_goals_by_team = px.bar(
    df_stats_goals_teams,
    x="Squad",
    y="Goals",
    title="Goal Scores by Teams",
    color="Squad",
)
fig_bar_goals_by_team.update_layout(xaxis_title="Team")
st.plotly_chart(fig_bar_goals_by_team, use_container_width=True)

col_groups1, col_groups2 = st.columns(2)
df_goals_by_position = (
    df_stats[["Goals", "Position"]]
    .groupby(by="Position", as_index=False)
    .sum()
    .query("Goals > 0")
    .sort_values(by=["Goals", "Position"], ascending=False)
)
fig_pie_goals_position = px.pie(
    df_goals_by_position,
    values="Goals",
    names="Position",
    title="Goals by Player Positions",
)
col_groups1.plotly_chart(fig_pie_goals_position, use_container_width=True)

df_stats_goals_nation = (
    df_stats[["Goals", "Nation"]]
    .groupby(by="Nation", as_index=False)
    .sum()
    .query("Goals > 0")
    .sort_values(by=["Goals", "Nation"], ascending=False)
)
fig_goals_nation = px.treemap(
    df_stats_goals_nation,
    path=["Nation"],  # Define a hierarquia; neste caso, apenas uma camada: Nation
    values="Goals",
    title="Goals by Nation",
)
col_groups2.plotly_chart(fig_goals_nation, use_container_width=True)

col_stats1, col_stats2, col_stats3 = st.columns(3)
col_stats1.subheader("Top 3 Players")
col_stats2.subheader("Top 3 Teams")
col_stats3.subheader("Top 3 Nations")
medals = [":first_place_medal:", ":second_place_medal:", ":third_place_medal:"]
for i in range(3):
    col_stats1.subheader(
        f"{medals[i]} {df_stats_goals_players['Player_Squad'].iloc[i].split(' - ')[0]}"
    )
    col_stats1.markdown(f":soccer: **{df_stats_goals_players['Goals'].iloc[i]}**")
    col_stats2.subheader(f"{medals[i]} {df_stats_goals_teams['Squad'].iloc[i]}")
    col_stats2.markdown(f":soccer: **{df_stats_goals_teams['Goals'].iloc[i]}**")
    col_stats3.subheader(f"{medals[i]} {df_stats_goals_nation['Nation'].iloc[i]}")
    col_stats3.markdown(f":soccer: **{df_stats_goals_nation['Goals'].iloc[i]}**")
