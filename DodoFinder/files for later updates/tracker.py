import urllib.request, json

url = urllib.request.urlopen("https://atlas.reznok.com/na_pvp_players.json")
data = json.loads(url.read().decode())

with open('players.json', 'w') as outfile:
    json.dump(data, outfile)