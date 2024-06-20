import streamlit as st
import oracledb
import sys
import pandas as pd
import plotly.express as px
from util.queries import select_logs

st.set_page_config(layout="wide", page_title="Health Status", page_icon=":helmet_with_white_cross:")

st.title(":helmet_with_white_cross: Health Status")

conn = st.connection("footstats", type="sql", autocommit=True)
df_logs = conn.query(select_logs)

st.header("Jobs Processed")

col1, col2 = st.columns([0.3, 0.7])
metrics = col1.container()

delta_days = (df_logs.loc[0, "process_date"] - df_logs.loc[1, "process_date"]).days
metrics.metric(
    label="Last Process",
    value=str(df_logs["process_date"].max().strftime("%Y-%m-%d %H:%M")),
    delta=delta_days,
)

delta_rows = int(df_logs.loc[0, "processed_rows"] - df_logs.loc[1, "processed_rows"])
metrics.metric(
    label="Processed Rows",
    value=str(df_logs.loc[0, "processed_rows"]),
    delta=delta_rows if (delta_rows != 0) else None,
)

delta_columns = int(df_logs.loc[0, "processed_columns"] - df_logs.loc[1, "processed_columns"])
metrics.metric(
    label="Processed Columns",
    value=str(df_logs.loc[0, "processed_columns"]),
    delta=delta_columns if (delta_columns != 0) else None,
)

# GRAPHIC
df_dates_processed = pd.DataFrame()
df_dates_processed["process_date_formatted"] = df_logs["process_date"].drop_duplicates()
df_dates_processed["process_date_formatted"] = df_dates_processed[
    "process_date_formatted"
].dt.strftime("%Y-%m-%d")

all_dates = pd.date_range(end=pd.Timestamp.today().date(), periods=5)[::-1]
all_dates = all_dates.strftime("%Y-%m-%d")
missing_dates_df = pd.DataFrame({"process_date_formatted": all_dates})

df_dates_processed["id"] = range(len(df_dates_processed))

merged_df = pd.merge(
    missing_dates_df,
    df_dates_processed,
    how="left",
    left_on="process_date_formatted",
    right_on="process_date_formatted",
)

merged_df["count"] = merged_df.groupby("process_date_formatted")["id"].transform(
    lambda x: x.notnull().cumsum()
)
max_count_df = merged_df.groupby("process_date_formatted")["count"].max().reset_index()

fig = px.line(
    max_count_df,
    x="process_date_formatted",
    y="count",
    title="Last 5 jobs",
)

fig.update_xaxes(type="date", tickformat="%Y-%m-%d", dtick=86400000.0)
fig.update_layout(xaxis_title="Date", yaxis_title="Count")

col2.plotly_chart(fig)

st.header("Logs")
st.dataframe(df_logs, hide_index=True, use_container_width=True)
