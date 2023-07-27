import csv

from common import STOCK_FILE_PATH, PREFERENCES_FILE_PATH

async def read_stock():
    """Reading stocks data from csv file

    Returns:
        list: list of stocks
    """
    with open(STOCK_FILE_PATH, 'r') as f:
        rows = f.readlines()
    
    rows = [x.split('\n')[0] for x in rows]

    return rows

async def add_stock(stock_name):
    """Adding new stock item to the csv file

    Args:
        stock_name (str): new stock symbol

    Returns:
        bool: stock is added sucessfully or not
    """
    rows = await read_stock()

    if not stock_name in rows:

        with open(STOCK_FILE_PATH, 'a') as f:

            write = csv.writer(f)
            write.writerows([[stock_name]])
        
        return True
    
    return False

async def remove_stock(stock_name):
    """Removing stock from the csv file

    Args:
        stock_name (str): stock symbol

    Returns:
        bool: stock is removed successfully or not
    """
    rows = await read_stock()

    if stock_name in rows:

        rows.remove(stock_name)

        rows = [[x] for x in rows]

        with open(STOCK_FILE_PATH, 'w') as f:

            write = csv.writer(f)
            write.writerows(rows)
        
        return True
    
    return False

async def get_preferences():
    """Reading saved preferences from the csv file
    like candle_size and duration 
    Returns:
        list: list of perferences
    """
    with open(PREFERENCES_FILE_PATH, 'r') as f:
        rows = f.readlines()
    
    rows = [x.split('\n')[0] for x in rows]

    return rows

async def update_preferences(candle_size, duration):
    """Updating perferences in the csv file

    Args:
        candle_size (str): duration between two datapoint
        duration (str): time period of data 
    """
    with open(PREFERENCES_FILE_PATH, 'w') as f:

            write = csv.writer(f)
            write.writerows([[candle_size], [duration]])