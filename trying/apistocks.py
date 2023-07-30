import requests
import pandas as pd
url = "https://apistocks.p.rapidapi.com/daily"

querystring = {"symbol":"MSFT","dateStart":"2023-07-01","dateEnd":"2023-07-31"}

headers = {
	"X-RapidAPI-Key": "7b0d7ffcf5msh2c3d7f26e39db7dp11f4bcjsna643d971a75c",
	"X-RapidAPI-Host": "apistocks.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()
second_key = list(data.keys())[1]
second_value = data[second_key]
second_value = pd.DataFrame(second_value)
df = second_value[['Date', 'Close']]

df.rename(columns={'Close': '4. close'}, inplace=True)
print(df.dtypes)