import requests
from bs4 import BeautifulSoup

url = "https://fbref.com/en/comps/676/schedule/UEFA-Euro-Scores-and-Fixtures"
urlData = requests.get(url)
#print(urlData.text) is just showing the raw html of the url.

soup = BeautifulSoup(urlData.text, "html.parser")
standingsTable = soup.select("table.stats_table")[0]
print(standingsTable)
