#import pandas as pd
import requests
import json

page = requests.get("https://membership.sportstg.com/results/getplayerpositions_match.cgi?aID=20551&mID=30326058")
tree = page.content

data = json.loads(tree)
urls = []
sww = []
 
#for element in data['PlayersNoPosition']:
for element in data['PlayersPosition']:
	urls.append("http://websites.sportstg.com/aj_swwid.cgi?playerID="+element[2]+"&assocID=10178")

for link in urls:
	page = requests.get(link)
	tree = page.content
	data = json.loads(tree)
	sww.append(data['swwPlayerID'])

print(sww)

#tables = pd.read_html("http://websites.sportstg.com/team_info.cgi?c=1-10178-171172-479810-24906261&a=STATS")
#print(tables[0])