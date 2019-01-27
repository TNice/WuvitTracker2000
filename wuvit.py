import discord
import urllib.request, json
import sched, time
import asyncio
from lxml import html
import requests

data = ""
s = sched.scheduler(time.time, time.sleep)

wuvitCo = {
    "Wuvit": ["N/A", False],
    "kweibs": ["N/A", False],
    "Brashnard": ["N/A", False]
}

tradingCoNames = ["Wuvit", "kweibs", "Brashnard"]

def UpdateWuvitName():
    page = requests.get("https://steamcommunity.com/profiles/76561198323881586")
    tree = html.fromstring(page.content)
    name = tree.xpath('//span[@class="actual_persona_name"]/text()')[0]
    tradingCoNames[0] = name
    print(tradingCoNames[0])

#returns most likely grid
#Note: More info on wuvits crew will help increase ability to guess his location
def DeterminWuvitCurrentLocation():
    brash = FindPlayer(tradingCoNames[2])

    possibleGrids = []
    
    #generate possible grids
    counter = 0
    probablyDurrationDelay = 60 #seconds
    for x in data["grids"]:
        for y in x["players"]:
            if tradingCoNames[0] == y["name"]:
                possibleGrids.append(x)
                if(brash[0] == x):
                    #compare durrations here
                    possibleGrids[counter].append(15)
                else:
                    possibleGrids[counter].append(0)
                counter += 1

    if len(possibleGrids) == 1
        return [possibleGrids[0], 100]


def DeterminWuvitBaseLocation():
    return null;

def FindPlayer(name):
    url = urllib.request.urlopen("https://atlas.reznok.com/na_pvp_players.json")
    data = json.loads(url.read().decode())
    for x in data["grids"]:
        for y in x["players"]:
            if name == y["name"]:
                return y["name"] + " is in " + x["grid"]

    return name + " is not online"

def FindPlayerRaw(name):
    url = urllib.request.urlopen("https://atlas.reznok.com/na_pvp_players.json")
    data = json.loads(url.read().decode())
    for x in data["grids"]:
        for y in x["players"]:
            if name == y["name"]:
                return [x["grid"], y["duration"]]

    return "N/A"

def GetTradingCompany():
    url = urllib.request.urlopen("https://atlas.reznok.com/na_pvp_players.json")
    data = json.loads(url.read().decode())
    found = [0, 0, 0]
    for x in data["grids"]:
        for y in x["players"]:
            if tradingCoNames[0] == y["name"]:
                if "123" != wuvitCo["Wuvit"][0]:
                    wuvitCo["Wuvit"][0] = x["grid"]
                    found[0] = 1
                else:
                    data = DeterminWuvitLocation()
                    found[0] = data[1]
                    wuvitCo["Wuvit"][0] = data[0]

            elif tradingCoNames[1] == y["name"]:
                wuvitCo["kweibs"][0] = x["grid"]
                found[1] = 1
            elif tradingCoNames[1] == y["name"]:
                wuvitCo["Brashnard"][0] = x["grid"]
                found[1] = 1

                
    wuvitCo["Wuvit"][1] = found[0]
    wuvitCo["kweibs"][1] = found[1]
    wuvitCo["Brashnard"][1] = found[2]

token = "NTM3MTE2OTQ3OTM1MDAyNjU0.Dygktw.ohiu8VFhjrydv7nCE70h36lOKf0"
client = discord.Client()

@client.event
async def on_message(message):
    content = message.content.lower()

    if "where" in content:
        if "trading company" in content:
            if(wuvitCo["Wuvit"][1] == True):
                await client.send_message(message.channel, "Wuvit is on " + wuvitCo["Wuvit"][0])
            else:
                await client.send_message(message.channel, "Wuvit last seen on " + wuvitCo["Wuvit"][0])

            if(wuvitCo["kweibs"][1] == True):
                await client.send_message(message.channel, "kweibs is on " + wuvitCo["kweibs"][0])
            else:
                await client.send_message(message.channel, "kweibs last seen on " + wuvitCo["kweibs"][0])

            if(wuvitCo["Brashnard"][1] == True):
                await client.send_message(message.channel, "Brashnard is on " + wuvitCo["Brashnard"][0])
            else:
                await client.send_message(message.channel, "Brashnard last seen on " + wuvitCo["Brashnard"][0])
                
        elif "dead sea" in content:
            await client.send_message(message.channel, FindPlayer("Spicy"))
        elif "black maya" in content:
            await client.send_message(message.channel, FindPlayer("Dryst"))
            
            

            
async def status_task():
    while True:
        GetTradingCompany()
        wuvit = "FUCK"
        if(wuvitCo["Wuvit"][1] == True):
            wuvit = "Wuvit is on " + wuvitCo["Wuvit"][0]
        else:
            wuvit = "Wuvit last seen on " + wuvitCo["Wuvit"][0]
                
        game = discord.Game(name=wuvit)
        print(wuvit)
        await client.change_presence(game=game)
        await asyncio.sleep(90)

async def name_task():
    while True:
        UpdateWuvitName()
        await asyncio.sleep(3600)
    
           
@client.event
async def on_ready():
    print(client.user.name + "Is Ready")
    client.loop.create_task(status_task())
    client.loop.create_task(name_task())
    UpdateWuvitName()

client.run(token)
