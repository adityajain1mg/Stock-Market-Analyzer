import csv

from common import STOCK_FILE_PATH


class StockDb:
    @classmethod
    async def read_stock(cls):
        """Reading stocks data from csv file and return list of stocks
        """
        with open(STOCK_FILE_PATH, 'r') as f:
            rows = f.readlines()
        
        rows = [x.split('\n')[0] for x in rows]

        return rows

    @classmethod
    async def add_stock(cls,stock_name):
        """Adding new stock item to the csv file
        """
        rows = await cls.read_stock()
        if not stock_name in rows:
            with open(STOCK_FILE_PATH, 'a') as f:

                write = csv.writer(f)
                write.writerows([[stock_name]])
            return "Stock successfully added to the list"
        return "Failed to add stock to the list"

    @classmethod
    async def remove_stock(cls,stock_name):
        """Removing stock from the csv file
        """
        rows = await cls.read_stock()

        if stock_name in rows:
            rows.remove(stock_name)
            rows = [[x] for x in rows]

            with open(STOCK_FILE_PATH, 'w') as f:
                write = csv.writer(f)
                write.writerows(rows)
            return "Stock successfully removed"
        return "Failed to remove, may be stock is not in the list"