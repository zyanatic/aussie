import pandas as pd
import requests
import json
from lxml import html
from bs4 import BeautifulSoup
import re

page = requests.get("http://websites.sportstg.com/round_info.cgi?c=1-10178-151184-391992-24906259&pool=&fixture=65922965&a=SELECT")
tree = page.content
soup = BeautifulSoup(tree,"html5lib")

# Get the URLs for home and away teams, later needed to construct URLs for each STATS page
soup = soup.find_all(href=re.compile("team_info"))
home_url = soup[2].get('href')
away_url = soup[4].get('href')

#--------------------------------------------------------------------------------------------------------------------------------------
# To-Do:
# To construct this URL https://membership.sportstg.com/results/getplayerpositions_match.cgi?aID=20551&mID=19926341
# that we use in the next step, we need to scrape aID, and mID using 
# <div style="display:none;" id="aid">10178</div> and <div class = "fixturerow" id = "extfix_19926341">
#--------------------------------------------------------------------------------------------------------------------------------------

# Get all pIDs, needed to construct URLs for swwPlayerIDs
def get_playerSWW():
	page = requests.get("https://membership.sportstg.com/results/getplayerpositions_match.cgi?aID=20551&mID=30326058")
	tree = page.content

	data = json.loads(tree)
	urls = []
	sww = []
	
# Construct the URLs we need to navigate to
	for element in data['PlayersPosition']:
		urls.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+element[2]+"&assocID=10178")

# Visit each URL and grab the swwPlayerID
	for link in urls:
		page = requests.get(link)
		tree = page.content
		data = json.loads(tree)
		sww.append(data['swwPlayerID'])
	return;

# This should get ALL tables on the page, each table can be selected by index tables[0] etc.
def get_tables():
	tables = pd.read_html("http://websites.sportstg.com/team_info.cgi?c=1-10178-171172-479810-24906261&a=STATS")
	return;
