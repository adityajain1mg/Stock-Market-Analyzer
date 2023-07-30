
STOCK_FILE_PATH = "db/stocks.csv"
STOCK_JSON_PATH = "db/stocks.json"
help = {
    "available urls": {
        "for help page": "/help",
        "for stocks historical data":"v1/analyse/historical?stock={}&duration={}&candle-size={}",
        "for comparing two stocks":"v1/analyse/compare?stock={}&stock={}&duration={}&candle-size={}",
        "for fetching realtime values of stocks":"v1/analyse/realtime?stock={}"
    },
    "available duration": {
        "1D": "use this for getting whole day stock prices",
        "1M": "use this for getting 1 months data",
        "3M": "use this for getting 3 months data",
        "6M": "use this for getting 6 months data",
        "1Y": "use this for getting 1 year data"
    },
    "available candle-size":{
        "1min": "use this to get 1 minute interval data",
        "5min": "use this to get 5 minute interval data",
        "15min": "use this to get 15 minute interval data",
        "30min": "use this to get 30 minute interval data",
        "60min": "use this to get 1 hour interval data",
        "1D": "use this to get 1 day interval data"
    }
}

api_list = ["alphavantage", "apistocks"]

apis = {
            "alphavantage":{
                "url": "https://alpha-vantage.p.rapidapi.com/query",
                "headers": {
                    "X-RapidAPI-Key": "7b0d7ffcf5msh2c3d7f26e39db7dp11f4bcjsna643d971a75c",
                    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
                }
            },
            "apistocks": {
                "url": "https://apistocks.p.rapidapi.com/daily",
                "headers": {
                    "X-RapidAPI-Key": "7b0d7ffcf5msh2c3d7f26e39db7dp11f4bcjsna643d971a75c",
                    "X-RapidAPI-Host": "apistocks.p.rapidapi.com"
                }
            }
        }

api_stats = {api: {'success': 0, 'failure': 0} for api in api_list}
