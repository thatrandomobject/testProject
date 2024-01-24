import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.cvmarket.lt/darbo-skelbimai?op=search&search%5Bjob_salary%5D=3&search%5Bcategories%5D%5B0%5D=8&search%5Bkeyword%5D=&ga_track=homepage&start=30'

response = requests.get(url)
print(response)