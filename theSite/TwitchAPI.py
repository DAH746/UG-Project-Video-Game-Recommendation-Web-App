from pprint import pprint

import theSite.views
import requests

# TODO WRONG ENDPOINT USED -> USE V2 (TwitchAPIv2.py)

def createAPIQueryForTwitch(gameName):

    urlBase = 'https://api.twitch.tv/kraken/search/streams?query='

    gameToBeSearched = gameName

    urlBase += gameToBeSearched

    urlBase += '&limit=3'  # default = 25 , max 100

    twitchAPIResponse = requests.get(urlBase,
                                     headers=theSite.views.twitchHeadersV2)

    twitchAPIResponseJSON = twitchAPIResponse.json()

    # pprint(twitchAPIResponseJSON)

    return twitchAPIResponseJSON

def returnTopThreeChannelsInformationForAGame(gameName):

    twitchAPIResponseJSON = createAPIQueryForTwitch(gameName)

    channelArrayList = [{},{},{}]

    relevantData = twitchAPIResponseJSON['streams']

    counter = 0

    for channel in relevantData:

        channelArrayList[counter]['channelName'] = channel['channel']['name']
        channelArrayList[counter]['linkToTheirTwitchStreamPage'] = channel['channel']['url']
        channelArrayList[counter]['twitchCategory'] = channel['game']
        channelArrayList[counter]['currentViewerCount'] = channel['viewers']
        channelArrayList[counter]['streamType'] = channel['stream_type']  # <- Constrains the type of streams returned.\
        # Valid values: live, playlist, all. Playlists are offline streams of VODs (Video on Demand) that appear live.\
        # Default: live.

        # For other attributes returned in call please see:
        # "Project\implementation\console output screenshots\twitch response for top streams for a given game"

        counter += 1

    # pprint(channelArrayList)

    return channelArrayList






