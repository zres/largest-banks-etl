# Largest Banks ETL Pipeline

ETL pipeline that scrapes the largest banks by market cap from Wikipedia,
transforms the values into multiple currencies, and stores the data in CSV and SQLite.

## Description

This project extracts data from a Wikipedia archive page listing the world's
largest banks by market capitalization. It then transforms the market cap values
from USD to GBP, EUR, and INR using exchange rates from a CSV file,
and loads the results into both a CSV file and a SQLite database.

## Features

- Scrapes bank data from Wikipedia using BeautifulSoup
- Converts market cap to GBP, EUR, and INR
- Saves output to CSV and SQLite database
- Logs progress with timestamps
- Runs SQL queries on the final database

## Technologies Used

- Python
- Pandas
- BeautifulSoup4
- Requests
- SQLite3

## Files

| File | Description |
|------|-------------|
| `banks_project.py` | Main ETL script |
| `exchange_rate.csv` | Input currency exchange rates |
| `Largest_banks_data.csv` | Output CSV file |
| `Banks.db` | Output SQLite database |
| `code_log.txt` | Progress log file |

## How to Run

1. Clone the repository
   git clone https://github.com/zres/largest-banks-etl.git

2. Install dependencies
   pip install requests pandas bs4 

3. Update your exchange_rate.csv file

4. Run the script
   python banks_project.py

## Output

The script produces market cap values in the following currencies:
- USD (original)
- GBP
- EUR
- INR
