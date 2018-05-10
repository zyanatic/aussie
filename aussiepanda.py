import pandas as pd
import requests
import json
from lxml import html
from bs4 import BeautifulSoup
import re
import os

playerlist = "D:/players.txt"

page = requests.get("http://websites.sportstg.com/round_info.cgi?c=1-10178-151184-478257-0&pool=1&fixture=69449576&a=SELECT")
tree = page.content
soup = BeautifulSoup(tree,"html5lib")

# Get the URLs for home and away teams, later needed to construct URLs for each STATS page
home_logo = soup.findAll('div', {'class' : 'hometeam'})
for div in home_logo:
    home_url = "http://websites.sportstg.com/" + div.find('a')['href']
away_logo = soup.findAll('div', {'class' : 'awayteam'})
for div in away_logo:
    away_url = "http://websites.sportstg.com/" + div.find('a')['href']
print(home_url)
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
	home_starting = []
	home_subs = []
	away_starting = []
	away_subs = []
	sww = []
	x = -1

# Construct the URLs we need to navigate to. starting and subs URLs are the same for each team, but it makes sense to keep them
# separated for later
	for pid in data['PlayersPosition']:
		x = x + 1
		if "Home" in str(data['PlayersPosition'][x][0]) and "Sub" not in str(data['PlayersPosition'][x][0]):
			home_starting.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+pid[2]+"&assocID="+aid)
		elif "Home" in str(data['PlayersPosition'][x][0]) and "Sub" in str(data['PlayersPosition'][x][0]):
			home_subs.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+pid[2]+"&assocID="+aid)
		elif "Away" in str(data['PlayersPosition'][x][0]) and "Sub" not in str(data['PlayersPosition'][x][0]):
			away_starting.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+pid[2]+"&assocID="+aid)
		elif "Away" in str(data['PlayersPosition'][x][0]) and "Sub" in str(data['PlayersPosition'][x][0]):
			away_subs.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+pid[2]+"&assocID="+aid)

# Visit each URL and grab the swwPlayerID and write them to a text file - This is probably useless, we need to pull all
# swwPlayerIDs anyway, as lineups always change, only pulling them once and saving to text file does not help. 
# Instead of just appending all IDs to one list, we need to do this for home_starting, home_subs, etc.
#
#	for link in home_url:
#		page = requests.get(link)
#		tree = page.content
#		data = json.loads(tree)
#		sww.append(data['swwPlayerID'])
#		with open(playerlist, "w") as csvfile:	
#			print(data['swwPlayerID'], file=csvfile)
	return;

# Checks if txt file with sww player ids already exists, if it's not there, executes the function. See above, probably not needed.
#if os.path.isfile(playerlist):
#	print("Player list already exists")
#else:
#	get_playerSWW()
get_playerSWW()

# This snippet should get ALL tables on the page, each table can be selected by index tables[0] etc.
def get_tables():
	tables = pd.read_html("http://websites.sportstg.com/team_info.cgi?c=1-10178-171172-479810-24906261&a=STATS")
	return;
