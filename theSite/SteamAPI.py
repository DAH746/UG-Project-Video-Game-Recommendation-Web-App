import pprint
import requests
import theSite.views

def createAndSendAPICall(gameIDObject):

    steamAllGames = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0002/')
    steamAllGames = steamAllGames.json()

    steamAllGamesJSON = steamAllGames['applist']['apps']


    gameName = gameIDObject.iGDBName  # will be placed into if statement below as more likely to be found in steam's api repsonse
    gameNameLength = len(gameName)  # So DLC's dont get picked up, so long as the lengths match
    gameFoundInSteamJson = False
    print('Steam API section -> the game thats being searched in JSON: ' + gameName)
##########
    # # To get total of items in list
    # count = 0
    # for game in steamAllGamesJSON:
    #
    #     count += 1
    #
    # print('Count total: ' + str(count))
##########
    count = 0
    for game in steamAllGamesJSON:
        count += 1
        if game['name'] == gameName and len(game['name']) == gameNameLength:
            print('\n' + gameName + ' was found on Steam. App ID: ' + str(game['appid']))
            print('A total of ' +str(count) + ' iterations were required to locate this game.\n')
            gameFoundInSteamJson = True
            gameIDObject.steamGameID = game['appid']
            break

    # print(steamAllGamesJSON)  # Print all contents of return steam catalogue contents

    steamAppId = gameIDObject.steamGameID

    steamStoreFrontResponse = requests.get('https://store.steampowered.com/api/appdetails?l=english&cc=gb&appids='+str(steamAppId))
    steamStoreFrontResponseJSON = steamStoreFrontResponse.json()

    if gameFoundInSteamJson == True:
        return steamStoreFrontResponseJSON
    else:   # Indicating not found
        steamStoreFrontResponseJSON = -1
        return steamStoreFrontResponseJSON
