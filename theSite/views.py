from django.contrib.sites import requests
from django.http import JsonResponse, QueryDict, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
# from requests import *
import requests
from pprint import pprint
import json
from django.template.defaulttags import register

from theSite import returnToFrontEnd
from theSite.tf_idf import tf_idf_function # remember "theSite."<mfunction>
import theSite.returnToFrontEnd

#   Twitch info
#   https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#oauth-client-credentials-flow
#   Look for "OAuth client credentials flow"
#   "expires_in": <number of seconds until the token expires>
#
#   Fair use (https://discuss.dev.twitch.tv/t/helix-rate-limit-for-streams-endpoint/12955):
#   Each client ID is granted a total of 30 queries per minute (if a Bearer token is not provided) or 120 queries per minute
#   (if a Bearer token is provided), across all new Twitch API queries.
#   If this limit is exceeded, an error is returned: HTTP 429 (Too Many Requests).

twitchBaseUrl = 'https://api.twitch.tv/helix/'

twitchClientId = 'Removed - <Enter Yours Here>'
twitchClientSecret = 'Removed - <Enter Yours Here>'
twitchOAuthRequest = requests.post('https://id.twitch.tv/oauth2/token?client_id=' + twitchClientId +
    '&client_secret=' + twitchClientSecret +
    '&grant_type=client_credentials'
    )

#twitchTokenType = twitchOAuthRequest.json().get("token_type") + " " #space added as thats a requirement for the formatting
twitchAccessToken = twitchOAuthRequest.json().get("access_token")

# twitchHeaders = {'Client-Id':'Client-Id: ' + twitchClientId, 'Authorization':'Authorization: Bearer ' + twitchAccessToken} # Example: "<apiURLforWhateverCall> 'Authorization: Bearer <OAuthCode> 'Client-Id: <clientID>'
# twitchHeadersTEST2 = {'Authorization':twitchAccessToken, 'Client-Id': twitchClientId}
# twitchHeadersTEST3= {'Authorization':'Authorization: Bearer ' + twitchAccessToken, 'Client-Id':'Client-Id: ' + twitchClientId}
# twitchHeadersTEST4 ={'Authorization':'Bearer ' + twitchAccessToken,'Client-Id': '' + twitchClientId}
# twitchHeadersTEST4 ={'Authorization':'Bearer ' + twitchAccessToken,'Client-Id':twitchClientId}
#   ^Final correct formatting - it's not what they were asking for, but its what they meant. 'twitchHeaders' is a duplicate of this line.
#   Code above is left to remind myself of what the errors are and what the correct formatting is.

twitchHeaders = {'Authorization': 'Bearer ' + twitchAccessToken, 'Client-Id': twitchClientId} # For IGDB mostly
twitchHeadersV2 = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-Id': twitchClientId} # For getting channel search
pprint(twitchAccessToken)
pprint(twitchHeaders)
# Code below is to with the COMMENTED OUT 'twitchHeaders' code above
# print("+-++-++-++-++-++-++-++-++-++-++-+\n")
# print('twitchHeader:')
# print(twitchHeaders)
# print('\n----------------------------------------------------')
# print(twitchHeadersTEST2)
# print('\n++++++++++++++++++++++++++++++++++++++++++++++++++++++')
# print(twitchHeadersTEST3)
# print("\n0000000000000000000000000000000000000")
# print(twitchHeadersTEST4)
# print("\n+-++-++-++-++-++-++-++-++-++-++-+\n")

#testing:
# HEADERS = {'client_id': twitchClientId}
# End twitch

# Headers = {'client-id': "d7l2w68fl3fsq0r58kzyapezxug0mg", 'Authorization': "Bearer " + ""

#  IGDB (Internet Game Database)

igdbHeaders = twitchHeaders.copy()  # IGDB is now owned by twitch, so now requires Twitch's authorization
igdbHeaders['Accept'] = 'application/json'  # In addition to the Authoriation & client id from Twitch, Accept is also
# a requirement
igdbHeaders['Client-ID'] = igdbHeaders.pop('Client-Id')
# pprint(twitchHeaders)
# print('----------------------------')
# pprint(igdbHeaders)

#   STEAM API:
#   My comments:
#   I will use IGDBs external steam api return value, rather than steam's methodology. Steam returns a massive
#   JSON file that contains ALL of their 'appid's (games) requires a massive loop to find the 'appid', when searching by name. The problem is not only
#   the time to attain the JSON file and to loop , but there are multiple entries by the same name, but have different expressions.
#   for example, DLC variations ('The Witcher 3: Wild Hunt: Blood and Wine'). It is far easier to get the appid with igdb
#   The only drawback however is an additional API call that needs to be made to IGDB - which has a limit of 4 per sec.

#   Documentation https://partner.steamgames.com/doc/webapi_overview

steamBaseUrl = 'http://api.steampowered.com/<interface name>/<method name>/v<version>/?key=CFDE187B9AF39CA1ADBA37B4BE87B3D5&format=json'

#   YOUTUBE API:
#   https://developers.google.com/youtube/v3/docs

googleApiKey = 'Removed - <Enter Yours Here>'
youtubeBaseUrlForVideoSearchUsingApi = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=20&q=<SEARCHTERM>&type=video&key=' + googleApiKey
# youtubeBaseUrlForVideoSearchUsingApi = 'https://www.googleapis.com/youtube/v3/search?part=snippet&order=viewCount&relevanceLanguage=en&regionCode=GB&maxResults=20&q=<SEARCHTERM>&type=video&key=' + googleApiKey
youtubeBaseUrlForVideoWatch = 'https://www.youtube.com/embed/'

@csrf_exempt
def index(request):
    return render(request, 'mainPage.html')

@csrf_exempt
def specificGameSearch(request):
    return render(request, 'searchForASpecificGame.html')

@csrf_exempt
def userInputtedGame(request):
    if request.is_ajax and request.method == "POST":
        # Input is "required" on frontend (<input>)
        inputRecievedFromFrontEnd = request.POST
        gameInputtedFromUser = inputRecievedFromFrontEnd['gameInputUser']

        print('\nGame received from front-end: ' +gameInputtedFromUser)  # Debug: prints input received from front-end

        testGame = returnToFrontEnd.returnRecommendedGame(gameInputtedFromUser)

        return JsonResponse({"status": 1, "recommendedGameArea": testGame}, status=200)

    return JsonResponse({"status": 0}, status=400)

@csrf_exempt
def test(request):

    # ----------------------------------    Twitch  ----------------------------------

    twitchGameTopRequestResponse = requests.get('https://api.twitch.tv/helix/games/top',
                                                headers=twitchHeaders)
    # print("********************************")
    # pprint(twitchOAuthRequest.json())
    #
    # print("\nFollowing is request.get call:\n")
    # pprint(twitchGameTopRequestResponse.json())
    # print("\n********************************")

    loader.get_template('test.html')

    twitchGameTopRequestResponseJSON = twitchGameTopRequestResponse.json()
    topCatagoryName = twitchGameTopRequestResponseJSON['data'][0]['name']
    # Following returns: https://static-cdn.jtvnw.net/ttv-boxart/Dead%20by%20Daylight-{width}x{height}.jpg
    topCatagoryBoxArt = twitchGameTopRequestResponseJSON['data'][0]['box_art_url']

    # Before: https://static-cdn.jtvnw.net/ttv-boxart/Dead%20by%20Daylight-{width}x{height}.jpg
    topCatagoryBoxArt = topCatagoryBoxArt.replace('{width}', '150')
    topCatagoryBoxArt = topCatagoryBoxArt.replace('{height}', '200')
    # After: https://static-cdn.jtvnw.net/ttv-boxart/Dead%20by%20Daylight-150x200.jpg

    context = {
        'twitchTopCatagoryName': topCatagoryName,
        'twitchTopCatagoryBoxArt': topCatagoryBoxArt,
    }

    # pprint(context)

    # ----------------------------------    IGDB    ----------------------------------

    igdbTopGamesIdNameRatingResponse = requests.post('https://api.igdb.com/v4/games',

                                          data='fields name, rating_count,summary, url,rating; where rating > 95; sort rating desc; '
                                               'rating_count; where rating_count > 1000;'
                                                ,

                                          headers=igdbHeaders
                                          )

    igdbTopGamesIdNameRatingResponseJSON = igdbTopGamesIdNameRatingResponse.json()
    # pprint(igdbTopGamesIdNameRatingResponseJSON)

    igdbTopGameName = igdbTopGamesIdNameRatingResponseJSON[0]['name']
    igdbTopGameRating = igdbTopGamesIdNameRatingResponseJSON[0]['rating']
    igdbTopGameId = igdbTopGamesIdNameRatingResponseJSON[0]['id']
    igdbTopGameRatingCount = igdbTopGamesIdNameRatingResponseJSON[0]['rating_count']
    igdbTopGameURL = igdbTopGamesIdNameRatingResponseJSON[0]['url']

    #todo tf idf testing - START

    igdbTopGameSummary = igdbTopGamesIdNameRatingResponseJSON[0]['summary']
    igdbGameTwoSummary = igdbTopGamesIdNameRatingResponseJSON[1]['summary'] #+"<similar words from first summary>"
    tf_idf_function(igdbTopGameSummary, igdbGameTwoSummary)

    # todo tf idf testing - END

    # pprint(igdbTopGamesIdNameRatingResponseJSON)

    igdbTopGamesCoverImageResponse = requests.post('https://api.igdb.com/v4/covers',
                                                   data='fields url,'
                                                        'game; where game=' +str(igdbTopGameId)+';'
                                                        ,
                                                   headers=igdbHeaders)

    igdbTopGamesCoverImageResponseJSON = igdbTopGamesCoverImageResponse.json()
    # pprint(igdbTopGamesCoverImageResponseJSON)
    igdbTopGameImageURL = igdbTopGamesCoverImageResponseJSON[0]['url']
    # See https://api-docs.igdb.com/?javascript#images, for all available image sizes (for line below)
    igdbTopGameImageURL = igdbTopGameImageURL.replace('thumb', 'cover_big_2x')

    context['igdbTopGameImageURL'] = igdbTopGameImageURL
    context['igdbTopGameName'] = igdbTopGameName
    context['igdbTopGameRating'] = round(igdbTopGameRating,2)
    context['igdbTopGameRatingCount'] = igdbTopGameRatingCount
    context['igdbTopGameURL'] = igdbTopGameURL

    # ----------------------------------    Steam    ----------------------------------

    steamAppIdFromIGDBResponse = requests.post('https://api.igdb.com/v4/external_games',
                                               data='fields uid, name, url;'
                                                    'category; where category=1;'
                                                    'game; where game=' +str(igdbTopGameId)+';'
                                                    ,
                                               headers=igdbHeaders)

    steamAppIdFromIGDBResponseJSON = steamAppIdFromIGDBResponse.json()

    steamAppId = steamAppIdFromIGDBResponseJSON[0]['uid']
    steamNameOnStorePage = steamAppIdFromIGDBResponseJSON[0]['name'] # This is for consistency sake, could use IGDB's name but this is for the unlikely case the name is displayed differently on steam
    generalUrlsForOtherPlatforms = steamAppIdFromIGDBResponseJSON
    #  ^ generalUrlsForOtherPlatforms <- is not needed right now, but contains twitch's url, good old games [gog], microsoft, giantbomb and youtubegaming [GAMING not the standard site!]
    steamAppUrl = 'https://store.steampowered.com/app/'+steamAppId

    steamStoreFrontResponse = requests.get('https://store.steampowered.com/api/appdetails?l=english&cc=gb&appids='+steamAppId)
    steamStoreFrontResponseJSON = steamStoreFrontResponse.json()

    # pprint(steamStoreFrontResponseJSON)

    steamGame = steamStoreFrontResponseJSON[steamAppId]['data']
    #Breaks down {'<uid>': {'data': { '<whatever_category>': <value>} to list of <whatever_category>

    steamGamePrice = steamGame['price_overview']['final_formatted']
    steamTotalRecommendationCount = steamGame['recommendations']['total']
    steamFirstVideoOnStoreFrontURL = steamGame['movies'][0]['mp4']['max']

    context['steamNameOnStorePage'] = steamNameOnStorePage
    context['steamGamePrice'] = steamGamePrice
    context['steamTotalRecommendationCount'] = steamTotalRecommendationCount
    context['steamFirstVideoOnStoreFrontURL'] = steamFirstVideoOnStoreFrontURL
    context['steamAppUrl'] = steamAppUrl

    # ---------------------------------    YouTube    ---------------------------------

    searchTermToBeQueriedOnYoutube = youtubeBaseUrlForVideoSearchUsingApi.replace('<SEARCHTERM>', steamNameOnStorePage)
    searchTermToBeQueriedOnYoutube = searchTermToBeQueriedOnYoutube.replace('maxResults=20', 'maxResults=3')

    youtubeSearchResponse = requests.get(searchTermToBeQueriedOnYoutube)
    youtubeSearchResponseJSON = youtubeSearchResponse.json()

    youtubeVideoList = {}  # New Dictionary

    for video in youtubeSearchResponseJSON['items']:

        youtubeVideoTitle = video['snippet']['title']
        videoId = video['id']['videoId']
        youtubeUrl = youtubeBaseUrlForVideoWatch + videoId  # Concat base youtube url with video id, to get complete URL

        youtubeVideoList[youtubeVideoTitle] = youtubeUrl

    # pprint(youtubeVideoList)
    context['youtubeVideoList'] = youtubeVideoList # Dict within dict

    return render(request, 'test.html', context)

@register.filter
def get_item(dictionary, key):
    #   https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
    return dictionary.get(key)
