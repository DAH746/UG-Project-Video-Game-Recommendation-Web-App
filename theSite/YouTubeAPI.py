import theSite.views
import requests
from pprint import pprint

def createAPIQueryForYouTube(gameName):
    youtubeBaseUrlForVideoSearchUsingApi = theSite.views.youtubeBaseUrlForVideoSearchUsingApi
    searchTermToBeQueriedOnYoutube = youtubeBaseUrlForVideoSearchUsingApi.replace('<SEARCHTERM>', gameName)
    searchTermToBeQueriedOnYoutube = searchTermToBeQueriedOnYoutube.replace('maxResults=20', 'maxResults=3')

    youtubeSearchResponse = requests.get(searchTermToBeQueriedOnYoutube)
    youtubeSearchResponseJSON = youtubeSearchResponse.json()

    return youtubeSearchResponseJSON

def returnListOfStoredVideos(gameName):

    youtubeSearchResponseJSON = createAPIQueryForYouTube(gameName)

    #pprint(youtubeSearchResponseJSON) # use to see if quota has been hit see -> https://console.developers.google.com/iam-admin/quotas

    youtubeVideoList = {}  # New Dictionary

    for video in youtubeSearchResponseJSON['items']:

        youtubeVideoTitle = video['snippet']['title']
        videoId = video['id']['videoId']
        youtubeUrl = theSite.views.youtubeBaseUrlForVideoWatch + videoId  # Concat base youtube url with video id, to get complete URL

        youtubeVideoList[youtubeVideoTitle] = youtubeUrl

    return youtubeVideoList