import requests
from pprint import pprint
import time

def getDetailsAboutGame(gameName, igdbHeaders):
    igdbGameInfoResponse = requests.post('https://api.igdb.com/v4/games',

                                         data='fields *; search "' + gameName + '";'
                                         ,

                                         headers=igdbHeaders
                                         )

    igdbGameInfoResponseJSON = igdbGameInfoResponse.json()
    # pprint(igdbGameInfoResponseJSON)
    return igdbGameInfoResponseJSON


def getCoverImageForGame(igdbGameJSON, igdbHeaders, gameIDObject):
    # Recommended game will be passed into here, where the id will be taken from the JSON and passed into another
    # IGDB api to grab the cover image for the video game

    igdbGameDetailsJSON = igdbGameJSON

    gameParamIdForIGDB = igdbGameDetailsJSON[0]['id']

    gameIDObject.iGDBgameID = gameParamIdForIGDB  # set ID within game ID object for a call later for Steam
    gameIDObject.iGDBHeaders = igdbHeaders  # set headers within obj
    getSteamIDFromIGDB(gameIDObject)  # get Steam ID and sort it here

    coverImageResponseForGameInParam = requests.post('https://api.igdb.com/v4/covers',
                                                     data='fields url,'
                                                          'game; where game=' + str(gameParamIdForIGDB) + ';'
                                                     ,
                                                     headers=igdbHeaders
                                                     )

    coverImageResponseForGameInParamJSON = coverImageResponseForGameInParam.json()

    coverImageResponseForGameInParamIGDBURL = coverImageResponseForGameInParamJSON[0]['url']

    coverImageResponseForGameInParamIGDBURL = coverImageResponseForGameInParamIGDBURL.replace('thumb', 'cover_big_2x')

    return coverImageResponseForGameInParamIGDBURL


def getRelatedGamesByGenre(igdbGameInfoResponseJSON, igdbHeaders):
    genresTheGameIsIn = igdbGameInfoResponseJSON[0]['genres']

    listOfGamesBasedOnGenre = []
    counterToDetermineWhenToSleep = 1

    for genre in genresTheGameIsIn:
        if counterToDetermineWhenToSleep % 3 == 0: # For each 3 loops, purpose is to not exceed 3 queries per sec for IGDB API
            print('\nLoop count is: ' + str(counterToDetermineWhenToSleep) + '. Sleep initiating for 1.5 seconds in the Genre Section.\n')
            time.sleep(1.5)
            print('Sleep Completed.\n')

        genreListOfGames = requests.post('https://api.igdb.com/v4/games',
                                         data='fields *;'
                                              'where genres = [' + str(genre) + '];'
                                              'limit 500;',
                                         headers=igdbHeaders
                                         )

        genreListOfGamesJSON = genreListOfGames.json()

        # pprint(genreListOfGamesJSON)

        listOfGamesBasedOnGenre += genreListOfGamesJSON

        counterToDetermineWhenToSleep += 1

    # print(genresTheGameIsIn)
    print('There were ' + str(counterToDetermineWhenToSleep-1) + ' Genres for ' + igdbGameInfoResponseJSON[0]['name'] + '.\n') # counterToDetermineWhenToSleep-1 as counter started at '1' not '0'
    print('There are a total of ' + str(len(listOfGamesBasedOnGenre)) + ' games produced from the Genre list.')
    # pprint(listOfGamesBasedOnGenre)


    # todo add in similar games too?
    return listOfGamesBasedOnGenre


def getSteamIDFromIGDB(gameIDObject):

    igdbID = gameIDObject.iGDBgameID
    igdbHeaders = gameIDObject.iGDBHeaders

    steamAppIdFromIGDBResponse = requests.post('https://api.igdb.com/v4/external_games',
                                               data='fields uid, name, url;'
                                                    'category; where category=1;'
                                                    'game; where game=' +str(igdbID)+';'
                                                    ,
                                               headers=igdbHeaders)

    steamAppIdFromIGDBResponseJSON = steamAppIdFromIGDBResponse.json()

    if steamAppIdFromIGDBResponseJSON == []:
        # Have to loop through steam's API 'ALL Game' response
        print("\nIGDB ERROR, STEAM ID COULD NOT BE FOUND.\n")

    steamAppId = steamAppIdFromIGDBResponseJSON[0]['uid']

    gameIDObject.steamGameID = steamAppId

    # No need to return anything as gameIDObject contains the ID
