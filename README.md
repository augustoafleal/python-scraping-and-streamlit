# Footstats

Scraping player statistics from the Brasileirão 2024 and displaying insights on a dashboard.

# Project Objective

1. Collect player statistics from the Brasileirão 2024.
2. ETL for data consolidation into historical and summary tables.
3. Display data on a dashboard.

# Project Structure

## Scraper
- Web scraping player statistics from the 2024 Brasileirão from [fbref.com](https://fbref.com/en/comps/24/stats/Serie-A-Stats).
- Loading data into a staging table and logging storage.
- Using the BeautifulSoup and SQLAlchemy libraries.

## Dashboard
- Developing a dashboard with Streamlit, featuring multiple pages.
- Utilizing libraries such as Plotly Express, Pandas, and Numpy.

## Database
- Modeling tables and procedures in Oracle Autonomous Database using Oracle Cloud Infrastructure.