

# Libraries
import discord
import os
import requests
import json
import time

client = discord.Client()


choice = input("Wil je de hardcoded access token gebruiken (y/n), gebruik y : ")

if choice == "N" or choice == "n":
	accessToken = input("wat is uw access token")
	accessToken = "Bearer " + accessToken
else:
	accessToken = "Bearer "your token here" "


r = requests.get(   "https://api.ciscospark.com/v1/rooms",
                    headers = {"Authorization": accessToken}
                )

if not r.status_code == 200:
    raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))



print("lijst van kanalen:")
rooms = r.json()["items"]
for room in rooms:
    print (room["title"])



while True:
    # Input the name of the room to be searched 
    roomNameToSearch = input("Welk kanaal moet er gefilterd worden? ")

    # Defines a variable that will hold the roomId 
    roomIdToGetMessages = None
    
    for room in rooms:
        # Searches for the room "title" using the variable roomNameToSearch 
        if(room["title"].find(roomNameToSearch) != -1):

            # Displays the rooms found using the variable roomNameToSearch (additional options included)
            print ("kanaal gevonden: " + roomNameToSearch)
            print(room["title"])

            # Stores room id and room title into variables
            roomIdToGetMessages = room["id"]
            roomTitleToGetMessages = room["title"]
            print("kanaal gevonden : " + roomTitleToGetMessages)
            break

    if(roomIdToGetMessages == None):
        print("Sorry, ik heb geen kanaal gevonden " + roomNameToSearch)
    else:
        break

def post_webex (message):
    responseMessage = message
    HTTPHeaders = { "Authorization": accessToken,"Content-Type": "application/json"}
    PostData = {"roomId": roomIdToGetMessages,"text": responseMessage}
    r = requests.post( "https://api.ciscospark.com/v1/messages", data = json.dumps(PostData), headers = HTTPHeaders)
    if not r.status_code == 200:
        raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        await message.channel.send('verzenden van data naar webex')
        post_webex (message.content)

client.run('your discord token here')
