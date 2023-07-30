from pandas.core.dtypes import dtypes
import requests
import pandas as pd

url = "https://alpha-vantage.p.rapidapi.com/query"

querystring = {"function":"TIME_SERIES_DAILY","symbol":"MSFT","outputsize":"compact","datatype":"json"}

headers = {
	"X-RapidAPI-Key": "7b0d7ffcf5msh2c3d7f26e39db7dp11f4bcjsna643d971a75c",
	"X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()
second_key = list(data.keys())[1]
second_value = data[second_key]
second_value = pd.DataFrame(second_value).T
second_value['Date'] = second_value.index
second_value
second_value['4. close'] = second_value['4. close'].astype(float)
df = second_value[['Date', '4. close']]
df.rename(columns={'4. close': 'Close'}, inplace=True)
print(df.dtypes)