import pandas as pd
import requests
from io import StringIO

# URL-адрес опубликованной Google Таблицы в формате CSV
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTHKgmSTdI0uGDzHCX0aiW5bBdwoOuh7sxI3M9NJkZB_bhwPwRQazYzfHZcFwvxXHXoJyqLL08k6t-A/pub?output=csv'
response = requests.get(url)
response.raise_for_status()

#Чтение CSV-данных из ответа и создание DataFrame
df = pd.read_csv(StringIO(response.text), index_col=0)