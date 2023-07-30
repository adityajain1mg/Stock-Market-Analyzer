import requests
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
url = "https://apistocks.p.rapidapi.com/daily"

symbol = 'IBM'
dateEnd = datetime.datetime.now().date()
dateStart = dateEnd - relativedelta(year=1)


querystring = {
	"symbol": symbol,
	"dateStart": dateStart,
	"dateEnd": dateEnd}

headers = {
	"X-RapidAPI-Key": "7b0d7ffcf5msh2c3d7f26e39db7dp11f4bcjsna643d971a75c",
	"X-RapidAPI-Host": "apistocks.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()
second_key = list(data.keys())[1]
second_value = data[second_key]
second_value = pd.DataFrame(second_value)
# df = second_value[['Date', 'Close']]

print(second_value)