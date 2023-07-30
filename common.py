import os
from dotenv import load_dotenv

load_dotenv()

period_function_mapping = {
    'min': "TIME_SERIES_INTRADAY",
    'D': "TIME_SERIES_DAILY",
    'W': "TIME_SERIES_WEEKLY",
    'M': "TIME_SERIES_MONTHLY"
}

STOCK_FILE_PATH = "db/stocks.csv"
PREFERENCES_FILE_PATH = "db/preferences.csv"

