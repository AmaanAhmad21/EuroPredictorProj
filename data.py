import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

url = "https://fbref.com/en/comps/676/stats/UEFA-Euro-Stats"
urlData = requests.get(url)
#print(urlData.text)  # is just showing the raw html of the url.

# Team links
soup = BeautifulSoup(urlData.text, "html.parser")
standingsTable = soup.select("table.stats_table")[0]
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

# Schedule links for teams.
soup1 = BeautifulSoup(htmlData, "html.parser")
links2 = soup1.find_all("a")
links2 = [l.get("href") for l in links2]
links2 = [l for l in links2 if l and "c676/schedule/" in l]
links2 = list(set(links2))  # removes duplicate links and making it a list removes the {} that sets automatically format.
links2 = ', '.join(links2)  # removes the [] that lists automatically formats and converts to a string, so that it can be formatted properly.
#print(links2)  # is showing the relative link for the Scores and fixtures of the Euro games.

euroUrls = [f"https://fbref.com{links2}"]
#print(euroUrls)  # is showing the absolute link for the scores and fixtures of the Euro games.

# Euro games stats.
euroUrl = euroUrls[0]
euroData = requests.get(euroUrl)
euroHtmlData = StringIO(euroData.text)  # This wraps the html data so the data is protected if panda gets updated.
euroGames = pd.read_html(euroHtmlData, match="UEFA Euro 2024")[0]
#print(euroGames)  # is showing the fixtures of the Euro games in a table format using pandas dataframe.

# Shooting links for Euro games.
soup2 = BeautifulSoup(euroHtmlData, "html.parser")
links3 = soup2.find_all("a")
links3 = [l.get("href") for l in links3]
links3 = [l for l in links3 if l and "c676/shooting/" in l]
links3 = list(set(links3))  # removes duplicate links and making it a list removes the {} that sets automatically format.
links3 = ', '.join(links3)  # removes the [] that lists automatically formats and converts to a string, so that it can be formatted properly.
#print(links3)  # is showing the relative link for the Scores and fixtures of the Euro games.

euroShootingUrls = [f"https://fbref.com{links3}"]
#print(euroShootingUrls)  # is showing the absolute link for the scores and fixtures of the Euro games.

# Euro games shooting stats.
euroShootingUrl = euroShootingUrls[0]
euroShootingData = requests.get(euroShootingUrl)
euroShootingHtmlData = StringIO(euroShootingData.text)  # This wraps the html data so the data is protected if panda gets updated.
euroShooting = pd.read_html(euroShootingHtmlData, match="Shooting")[0]
euroShooting.columns = euroShooting.columns.droplevel()  # Removes first index level thats not needed.
#print(euroShooting)  # is showing the Shooting stats of the Euro games in a table format using pandas dataframe.
