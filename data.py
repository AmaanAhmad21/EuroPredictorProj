import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

url = "https://fbref.com/en/comps/676/stats/UEFA-Euro-Stats"
urlData = requests.get(url)
#print(urlData.text)  #is just showing the raw html of the url.

soup = BeautifulSoup(urlData.text, "html.parser")
standingsTable = soup.select("table.stats_table")[0]
#print(standingsTable)  #is showing the filtered html of stats_table.

links = standingsTable.findAll("a")
links = [l.get("href") for l in links]
links = [l for l in links if "/squads/" in l]
#print(links)  #is showing the links of each team.

teamUrls = [f"https://fbref.com{l}" for l in links]
#print(teamUrls)  #is showing the absolute links for each team.

teamUrl = teamUrls[0]
data = requests.get(teamUrl)
htmlData = StringIO(data.text)  # This wraps the html data so the data is protected if panda gets updated.
matches = pd.read_html(htmlData, match="Scores & Fixtures")
#print(matches[0])  #is showing the fixtures in a table format using pandas dataframe.

