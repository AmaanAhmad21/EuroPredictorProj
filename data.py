import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

url = "https://fbref.com/en/comps/676/stats/UEFA-Euro-Stats"
urlData = requests.get(url)
#print(urlData.text)  # is just showing the raw html of the url.

soup = BeautifulSoup(urlData.text, "html.parser")
standingsTable = soup.select("table.stats_table")[0]
#print(standingsTable)  # is showing the filtered html of stats_table.

links = standingsTable.findAll("a")
links = [l.get("href") for l in links]
links = [l for l in links if "/squads/" in l]
#print(links)  # is showing the relative links of each team.

teamUrls = [f"https://fbref.com{l}" for l in links]
#print(teamUrls)  # is showing the absolute links for each team.

teamUrl = teamUrls[0]
teamData = requests.get(teamUrl)
htmlData = StringIO(teamData.text)  # This wraps the html data so the data is protected if panda gets updated.
matches = pd.read_html(htmlData, match="Scores & Fixtures")
#print(matches[0])  # is showing the fixtures in a table format using pandas dataframe.

soup = BeautifulSoup(htmlData, "html.parser")
links2 = soup.find_all("a")
links2 = [l.get("href") for l in links2]
links2 = [l for l in links2 if l and "c676/schedule/" in l]
links2 = list(set(links2))  # removes duplicate links.
links2 = ', '.join(links2)  # removes the {} that set automatically formats, so that the euroUrls can be formatted properly.
#print(links2)  # is showing the relative link for the Scores and fixtures of the Euro games.

euroUrls = [f"https://fbref.com{links2}"]
#print(euroUrls)  # is showing the absolute link for the scores and fixtures of the Euro games.