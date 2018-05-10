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

# Get the aID / assocID
# For games between teams from different associations (e.g. cup, friendly) we will have to see if we can get each teams aID separately
aid = soup.find(id="aid").get_text()

# This grabs the URL used to get the lineups
selteam = soup.find_all(attrs={"data-selteam":True})
for a in selteam:
	getplayerpositions_match = a['data-selteam']

# Get all pIDs, needed to construct URLs for swwPlayerIDs
def get_playerSWW():
	page = requests.get(getplayerpositions_match)
	tree = page.content
	data = json.loads(tree)
	home_starting_url = []
	home_subs_url = []
	away_starting_url = []
	away_subs_url = []
	home_starting = []
	home_subs = []
	away_starting = []
	away_subs = []
	sww = []
	x = -1

# Construct the URLs we need to navigate to
	for pid in data['PlayersPosition']:
		x = x + 1
		if "Home" in str(data['PlayersPosition'][x][0]) and "Sub" not in str(data['PlayersPosition'][x][0]):
			home_starting_url.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+pid[2]+"&assocID="+aid)
		elif "Home" in str(data['PlayersPosition'][x][0]) and "Sub" in str(data['PlayersPosition'][x][0]):
			home_subs_url.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+pid[2]+"&assocID="+aid)
		elif "Away" in str(data['PlayersPosition'][x][0]) and "Sub" not in str(data['PlayersPosition'][x][0]):
			away_starting_url.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+pid[2]+"&assocID="+aid)
		elif "Away" in str(data['PlayersPosition'][x][0]) and "Sub" in str(data['PlayersPosition'][x][0]):
			away_subs_url.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+pid[2]+"&assocID="+aid)

# Visit each URL and grab the swwPlayerID. Maybe this can be done more efficiently?
	for link in home_starting_url:
		page = requests.get(link)
		tree = page.content
		data = json.loads(tree)
		home_starting.append(data['swwPlayerID'])

	for link in home_subs_url:
		page = requests.get(link)
		tree = page.content
		data = json.loads(tree)
		home_subs.append(data['swwPlayerID'])

	for link in home_starting_url:
		page = requests.get(link)
		tree = page.content
		data = json.loads(tree)
		away_starting.append(data['swwPlayerID'])

	for link in home_starting_url:
		page = requests.get(link)
		tree = page.content
		data = json.loads(tree)
		away_subs.append(data['swwPlayerID'])	

# Printing to text file does not help us, as lineups always change and we are only getting lists of IDs of players who are in the lineup
#	print(home_starting)
#		with open(playerlist, "w") as csvfile:	
#			print(data['swwPlayerID'], file=csvfile)
	return;

# Checks if txt file with sww player ids already exists, if it's not there, executes the function
#if os.path.isfile(playerlist):
#	print("Player list already exists")
#else:
#	get_playerSWW()
get_playerSWW()

# This snippet should get ALL tables on the page, each table can be selected by index tables[0] etc.
def get_tables():
	tables = pd.read_html("http://websites.sportstg.com/team_info.cgi?c=1-10178-171172-479810-24906261&a=STATS")
	return;
