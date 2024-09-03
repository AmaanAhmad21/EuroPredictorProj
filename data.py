import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time

url = "https://fbref.com/en/comps/676/stats/UEFA-Euro-Stats"
urlData = requests.get(url)

# Team links
soup = BeautifulSoup(urlData.text, "html.parser")
standingsTable = soup.select("table.stats_table")[0]
links = standingsTable.find_all("a")
links = [l.get("href") for l in links]
links = [l for l in links if "/squads/" in l]
teamUrls = [f"https://fbref.com{l}" for l in links]

allMatches = []


for i in teamUrls:
    teamName = i.split("/")[-1].replace("-Men-Stats", "")
    teamData = requests.get(i)
    htmlData = StringIO(teamData.text)
    time.sleep(1)
    matches = pd.read_html(htmlData, match="Scores & Fixtures")
    time.sleep(2)

    # Schedule links for Euro teams.
    soup1 = BeautifulSoup(htmlData, "html.parser")
    links2 = soup1.find_all("a")
    links2 = [l.get("href") for l in links2]
    links2 = [l for l in links2 if l and "c676/schedule/" in l]
    links2 = list(set(links2))  # removes duplicate links and making it a list removes the {} that sets automatically format.
    links2 = ', '.join(links2)  # removes the [] that lists automatically formats and converts to a string, so that it can be formatted properly.
    euroUrls = [f"https://fbref.com{links2}"]
    time.sleep(2)

    for j in euroUrls:
        time.sleep(1)
        # Euro games stats.
        euroData = requests.get(j)
        euroHtmlData = StringIO(euroData.text)  # This wraps the html data so the data is protected if panda gets updated.
        euroGames = pd.read_html(euroHtmlData, match="UEFA Euro 2024")[0]
        time.sleep(1)

        # Shooting links for Euro games.
        soup2 = BeautifulSoup(euroHtmlData, "html.parser")
        links3 = soup2.find_all("a")
        links3 = [l.get("href") for l in links3]
        links3 = [l for l in links3 if l and "c676/shooting/" in l]
        links3 = list(set(links3))  # removes duplicate links and making it a list removes the {} that sets automatically format.
        links3 = ', '.join(links3)  # removes the [] that lists automatically formats and converts to a string, so that it can be formatted properly.
        euroShootingUrls = [f"https://fbref.com{links3}"]
        time.sleep(1)

        # Euro games shooting stats.
        euroShootingUrl = euroShootingUrls[0]
        euroShootingData = requests.get(euroShootingUrl)
        euroShootingHtmlData = StringIO(euroShootingData.text)  # This wraps the html data so the data is protected if panda gets updated.
        euroShooting = pd.read_html(euroShootingHtmlData, match="Shooting")[0]
        euroShooting.columns = euroShooting.columns.droplevel()  # Removes first index level thats not needed.
        time.sleep(1)

        # Merge Euro matches and shooting data.
        try:
            euroTeamData = euroGames.merge(euroShooting[["Date", "Gls", "Sh", "SoT", "FK", "PK", "PKatt"]], on="Date")
            euroTeamData["Team"] = teamName  # adds a team name column to data.
            time.sleep(2)
        except ValueError:
            continue

        allMatches.append(euroTeamData)
        time.sleep(1)

matchData = pd.concat(allMatches)
print(matchData)
matchData.to_csv("matches.csv")
