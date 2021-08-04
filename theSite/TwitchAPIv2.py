from pprint import pprint

import theSite.views
import requests

def getTwitchGameIdForGame(gameName):
    urlBase = 'https://api.twitch.tv/helix/games?name='
    urlBase += gameName

    twitchAPIResponse = requests.get(urlBase,
                                     headers=theSite.views.twitchHeaders)

    twitchAPIResponseJSON = twitchAPIResponse.json()

    gameId = twitchAPIResponseJSON['data'][0]['id']

    return gameId


def createAPIQueryForTwitch(gameName):
    urlBase = 'https://api.twitch.tv/helix/streams?'

    twitchGameId = 'game_id=' + str(getTwitchGameIdForGame(gameName))
    amountToBeReturned = 'first=3&'  # Maximum number of objects to return. Maximum: 100. Default: 20.

    urlBase += amountToBeReturned
    urlBase += twitchGameId

    # print(urlBase + '\n')

    twitchAPIResponse = requests.get(urlBase,
                                     headers=theSite.views.twitchHeaders)

    twitchAPIResponseJSON = twitchAPIResponse.json()

    return twitchAPIResponseJSON


def returnTopThreeChannelsInformationForAGame(gameName):

    twitchAPIResponseJSON = createAPIQueryForTwitch(gameName)

    channelArrayList = [{}, {}, {}]

    relevantData = twitchAPIResponseJSON['data']

    counter = 0

    for channel in relevantData:
        channelArrayList[counter]['channelName'] = channel['user_login']
        channelArrayList[counter]['channelDisplayName'] = channel['user_name']
        channelArrayList[counter]['twitchCategory'] = channel['game_name']
        channelArrayList[counter]['currentViewerCount'] = channel['viewer_count']
        channelArrayList[counter]['streamType'] = channel['type']
        channelArrayList[counter]['streamTitle'] = channel['title']
        # https://dev.twitch.tv/docs/api/reference#get-streams
        counter += 1

    return channelArrayList
