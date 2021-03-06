import discord
import urllib.request, json
import sched, time
import asyncio
from lxml import html
import requests

data = ""
s = sched.scheduler(time.time, time.sleep)

grid = {}
grid["grids"] = {}

usersToNotify = {}

gridSpaces = [
    'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15',
    'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15',
    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15',
    'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15',
    'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15',
    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15',
    'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15',
    'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13', 'H14', 'H15',
    'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'I11', 'I12', 'I13', 'I14', 'I15',
    'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10', 'J11', 'J12', 'J13', 'J14', 'J15',
    'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'K10', 'K11', 'K12', 'K13', 'K14', 'K15',
    'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10', 'L11', 'L12', 'L13', 'L14', 'L15',
    'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 'M13', 'M14', 'M15',
    'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10', 'N11', 'N12', 'N13', 'N14', 'N15',
    'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'O9', 'O10', 'O11', 'O12', 'O13', 'O14', 'O15'
]

def SaveGridStates():
    url = urllib.request.urlopen("https://atlas.reznok.com/na_pvp_players.json")
    data = json.loads(url.read().decode())
    count = 0
    for x in data["grids"]:
        data["grids"][count] = []
        for y in x["players"]:
            data["grids"][count].append({
                'name': y["name"]
            })
        count += 1
    
    outfile = open('lastState.json', 'w')  
    json.dump(data, outfile)
    print("Grids State Saved")

def LoadUsersToNotify():
    usersToNotify.clear()
    file = open("notifyUsers.txt", 'r')
    for line in file:
        usersToNotify.append(line)
    file.close()
    print("Notification List Loaded")

def SaveUsersToNotify():
    file = open("notifyUsers.txt", 'w')
    for user in usersToNotify:
        file.write(user)
    print("Notification List Saved")

def GetUsersInRegion(region):
    url = urllib.request.urlopen("https://atlas.reznok.com/na_pvp_players.json")
    data = json.loads(url.read().decode())
    
    players = [] 
    for x in data["grids"]:
       if x["grid"] == region:
        for y in x["players"]:
            players.append(y['name'])
    
    return players

def GetNewUsers(region):
    if region == "N/A":
        return
    newUsers = []
    try:
        index = gridSpaces.index(region)
       
        with open("lastState.json") as file:
            data = json.load(file)
            for new in GetUsersInRegion(region):
                isnew = True
                for old in data['grids'][index]:
                   if new == old:
                       isnew = False
                       break
                if isnew == True:
                    newUsers.append(new)
    except:
        print("Failed To Gather Either New Or Old State")

    return newUsers

def FindPlayer(name):
    url = urllib.request.urlopen("https://atlas.reznok.com/na_pvp_players.json")
    data = json.loads(url.read().decode())
    for x in data["grids"]:
        for y in x["players"]:
            if name == y["name"]:
                return x["grid"]

    return "N/A"

def Exit():
    SaveUsersToNotify()
    SaveGridStates()
    exit(1)

token = "NTM3MTE2OTQ3OTM1MDAyNjU0.Dygktw.ohiu8VFhjrydv7nCE70h36lOKf0"
client = discord.Client()

@client.event
async def on_message(message):
    return
                    
async def status_task():
    isFirst = True
    while True:
        if isFirst != True:
            for user in usersToNotify:
                newUsers = GetNewUsers(FindPlayer(user))
                if len(newUser) != 0:
                    #sends message to user

        isFirst = False
        await asyncio.sleep(90)
            
@client.event
async def on_ready():
    print(client.user.name + "Is Ready")
    #client.loop.create_task(status_task())
    LoadUsersToNotify()
    SaveGridStates()

client.run(token)
