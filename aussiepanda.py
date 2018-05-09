import pandas as pd
import requests
import json
from lxml import html
from bs4 import BeautifulSoup
import re
import os

playerlist = "D:/players.txt"

page = requests.get("http://websites.sportstg.com/round_info.cgi?c=1-10178-151184-391992-24906259&pool=&fixture=65922965&a=SELECT")
tree = page.content
soup = BeautifulSoup(tree,"html5lib")

# Get the URLs for home and away teams, later needed to construct URLs for each STATS page
# This can possibly be improved for flexibility
team_info = soup.find_all(href=re.compile("team_info"))
home_url = team_info[2].get('href')
away_url = team_info[4].get('href')

# Get the aID / assocID
# For games between teams from different associations (e.g. cup, friendly) we will have to see if we can get each teams aID separately
aid = soup.find(id="aid").get_text()

# This grabs the URL used to get the lineups
selteam = soup.find_all(attrs={"data-selteam":True})
for a in selteam:
	getplayerpositions_match = a['data-selteam']

# Get all pIDs, needed to construct URLs for swwPlayerIDs
#--------------------------------------------------------------------------------------------------------------------------------------
# To-Do: 
# Instead of just grabbing the swwPlayerIDs and adding them to the SAME list, we need to use separate lists for 
# home_starting, home_subs, away_starting, away_subs. (Alternatively dictionary?) This is necessary, because we need to compare
# each Teams swwPlayerIDs with their respective STATS page
#--------------------------------------------------------------------------------------------------------------------------------------
def get_playerSWW():
	page = requests.get(getplayerpositions_match)
	tree = page.content

	data = json.loads(tree)
	urls = []
	sww = []

# Construct the URLs we need to navigate to
	for pid in data['PlayersPosition']:
		# Here is where we need aID (same as assocID) again
		urls.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+pid[2]+"&assocID="+aid)

# Visit each URL and grab the swwPlayerID and write them to a text file
	for link in urls:
		page = requests.get(link)
		tree = page.content
		data = json.loads(tree)
		sww.append(data['swwPlayerID'])
		with open(playerlist, "a") as csvfile:	
			print(data['swwPlayerID'], file=csvfile)
	return;

# Checks if txt file with sww player ids already exists, if it's not there, executes the function
if os.path.isfile(playerlist):
	print("Player list already exists")
else:
	get_playerSWW()


# This snippet should get ALL tables on the page, each table can be selected by index tables[0] etc.
def get_tables():
	tables = pd.read_html("http://websites.sportstg.com/team_info.cgi?c=1-10178-171172-479810-24906261&a=STATS")
	return;
