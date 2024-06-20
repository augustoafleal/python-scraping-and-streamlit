from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import os
import oracledb
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import datetime

URL = "https://fbref.com/en/comps/24/stats/Serie-A-Stats"
TABLE_NAME = "footstats_staging_playerstats_brasileirao"
LOG_TABLE_NAME = "footstats_logs"


def message(text):
    datetime_utc = datetime.utcnow().strftime("%Y%m%d %H:%M:%S")
    print(f"> {datetime_utc} - {text}")


def load_html(url):
    message(f"Loading HTML from {URL}")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(10)
    html_content = driver.page_source
    driver.quit()

    return html_content


def df_raw(html_content):
    message("Generating dataframe")
    data = BeautifulSoup(html_content, "html.parser")
    table_class = "min_width sortable stats_table shade_zero now_sortable sticky_table eq2 re2 le2"
    target_table = data.find("table", class_=table_class)

    if target_table:
        table_html = StringIO(str(target_table))
        df = pd.read_html(table_html, header=1)[0]
    else:
        raise ValueError("HTML table not found.")
    return df


def df_sanitizer(df):
    message("Sanitizing dataframe")
    df = df.drop(df[df["Player"] == "Player"].index)
    df["Nation"] = df["Nation"].str[-3:]
    df["Age"] = df["Age"].str[:-4]
    df.drop(columns=["Matches"], inplace=True)
    df.drop(columns=["Rk"], inplace=True)
    df["CREATED_DATE"] = pd.Timestamp.utcnow()

    return df


def engine_creator():
    message("Creating database engine")
    load_dotenv()

    username = os.environ.get("user")
    password = os.environ.get("password")
    cs = os.environ.get("cs")

    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=cs,
    )

    engine = create_engine("oracle+oracledb://", creator=lambda: connection)
    return engine


def database_persist(engine, df_sanitized, TABLE_NAME):
    message(f"Persisting dataframe to table {TABLE_NAME}")
    df_sanitized.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)


def df_log_generator(shape_tuple):
    message(f"Generating log")
    data_log = {
        "PROCESSED_ROWS": [shape_tuple[0]],
        "PROCESSED_COLUMNS": [shape_tuple[1]],
        "SCRIPT_FILE": [os.path.basename(__file__)],
        "TABLE_LOADED": [TABLE_NAME],
        "PROCESS_DATE": [pd.Timestamp.utcnow()],
    }
    return pd.DataFrame(data_log)


def database_persist_log(engine, df_log, LOG_TABLE_NAME):
    message(f"Persisting log dataframe to table {LOG_TABLE_NAME}")
    df_log.to_sql(LOG_TABLE_NAME, engine, if_exists="append", index=False)


def main():
    html_content = load_html(URL)
    df = df_raw(html_content)
    df_sanitized = df_sanitizer(df)
    df_log = df_log_generator(df_sanitized.shape)
    engine = engine_creator()
    database_persist(engine, df_sanitized, TABLE_NAME)
    database_persist_log(engine, df_log, LOG_TABLE_NAME)


main()
