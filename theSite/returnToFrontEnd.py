from pprint import pprint

import theSite.views
import theSite.IGDBapi
import theSite.YouTubeAPI
import theSite.TwitchAPI
import theSite.TwitchAPIv2
import theSite.TempGameIDContainerObject
import theSite.SteamAPI
import theSite.RecommendationAlgorithm

def returnRecommendedGame(nameOfGameForTheRecommendationToBeBasedOffOf):

    gameIDObject = theSite.TempGameIDContainerObject.TempGameIDContainerObject()

    htmlReturnStringBuilder = '<div class="container-fluid"> ' \
                              '<p class="mb-4 pb-3 border-bottom text-left">'

    if nameOfGameForTheRecommendationToBeBasedOffOf[0] == '/':
        skipRecommendation = True
        nameOfGameForTheRecommendationToBeBasedOffOf = nameOfGameForTheRecommendationToBeBasedOffOf[1:]
    else:
        skipRecommendation = False

    htmlReturnStringBuilder = createIGDBHTMLCode(htmlReturnStringBuilder,
                                                 nameOfGameForTheRecommendationToBeBasedOffOf,
                                                 gameIDObject,
                                                 skipRecommendation)

    recommendedGame = gameIDObject.iGDBName

    htmlReturnStringBuilder = createYouTubeHTMLCode(htmlReturnStringBuilder, recommendedGame)

    htmlReturnStringBuilder = createTwitchHTMLCode(htmlReturnStringBuilder, recommendedGame)

    htmlReturnStringBuilder = createSteamHTMLCode(htmlReturnStringBuilder, gameIDObject)

    print('\nHTML CODE GENERATED:\n\n' + htmlReturnStringBuilder + '\n')  # Prints HTML code that will be sent to frontend

    return htmlReturnStringBuilder


def createSteamHTMLCode(htmlReturnStringBuilder, gameIDObject):
    htmlReturnStringBuilder += '<H5 class="mb-4 pb-2"> Here is some final parts of ' \
                               'information, and a purchasing option, from <strong>Steam</strong>!</h5>'

    steamStoreFrontResponseJSON = theSite.SteamAPI.createAndSendAPICall(gameIDObject)

    # pprint(steamStoreFrontResponseJSON)

    if steamStoreFrontResponseJSON == -1:   # -1 indicates game wasn't located in Steam's JSON response

        htmlReturnStringBuilder += 'Unfortunately this game is currently not available on Steam at this ' \
                                   'moment in time.'
        return htmlReturnStringBuilder

    steamAppId = gameIDObject.steamGameID

    steamAppUrl = 'https://store.steampowered.com/app/' + str(gameIDObject.steamGameID)  # External link to Steam

    steamGameURLBuilder = '<a href="' + steamAppUrl + '">' + steamAppUrl + '</a>'

    steamGame = steamStoreFrontResponseJSON[str(steamAppId)]['data']
    isThisSteamGameFree = steamGame['is_free']  # Contains boolean value

    isThisGameComingSoonToTheStore = steamGame['release_date']['coming_soon']

    if isThisGameComingSoonToTheStore is True:
        theDateTheGameIsComingToTheStore = steamGame['release_date']['date']

    gameName = gameIDObject.iGDBName
    try:

        if isThisSteamGameFree == True:
            htmlReturnStringBuilder += 'Steam is currently offering this game <strong>free of charge</strong>!<p></p>'
        else:
            steamGamePrice = steamGame['price_overview']['final_formatted']
            htmlReturnStringBuilder += 'Steam is currently charging <strong>' + str(steamGamePrice)+'</strong> for ' \
                                        + gameName+'!<p></p>'

        steamTotalReviewsCount = steamGame['recommendations']['total']

        htmlReturnStringBuilder += 'A total of <strong>' + str(steamTotalReviewsCount) + '</strong> Steam users have' \
                                 ' provided ' + gameName + ' with a review! <p></p>'

        steamFirstVideoOnStoreFrontURL = steamGame['movies'][0]['mp4']['max']

        htmlReturnStringBuilder += 'Here is the <strong>first video on Steam\'s storefront</strong> for '\
                                    + gameName + ':<p></p>'
        htmlReturnStringBuilder += '<div class="row"><div class="col-sm">'

        htmlReturnStringBuilder += '<div class="d-flex justify-content-center"><video width="500" controls>' \
                                    + '<source src="' + str(steamFirstVideoOnStoreFrontURL) + '" type="video/mp4">' \
                                    + '</video></div><p></p>'

        htmlReturnStringBuilder += 'If you are interested in purchasing this game on Steam, please visit: <strong>' \
                                    + steamGameURLBuilder + '</strong>! </div></div>'


    except KeyError as e:
        print("STEAM KEY ERROR:\n")
        print(e)

        if isThisGameComingSoonToTheStore is False:
            # This means the game has been taken off the Steam store, or is unavailable
            htmlReturnStringBuilder += ''
        # Test for "days gone" where --> https://store.steampowered.com/app/1259420/Days_Gone/


    return htmlReturnStringBuilder


def createTwitchHTMLCode(htmlReturnStringBuilder, nameOfGameThatHasBeenRecommended):
    twitchChannelDetails = theSite.TwitchAPIv2.returnTopThreeChannelsInformationForAGame(nameOfGameThatHasBeenRecommended)

    htmlReturnStringBuilder += '<H5 class="mb-4 pb-2">Here are the three <strong>currently</strong> most watched streams on ' \
                               '<strong>Twitch</strong> for <strong style="color:blue">' \
                               + nameOfGameThatHasBeenRecommended + '!</strong></h5>'

    if twitchChannelDetails[0].get('twitchCategory') is None:
        htmlReturnStringBuilder += 'If you are seeing this, then unfortunately there are <strong>no</strong> ' \
                                   ' streamers streaming this game live on <strong>Twitch</strong> at this time.'

        htmlReturnStringBuilder += '<p class="mb-4 pb-4 border-bottom text-center"></div></div>'
        return htmlReturnStringBuilder

    htmlReturnStringBuilder += 'These streams are produced when viewing a "Twitch Category" under the name '\
                               + '<strong>' + twitchChannelDetails[0]['twitchCategory'] + '</strong>, where it has been sorted' \
                               + ' by "<strong>Viewers (High to Low)</strong>" on their web application. <p></p>'

    htmlReturnStringBuilder += '<div class="row"><div class="col-sm">'

    twitchEmbedDetails = '<iframe src="https://player.twitch.tv/?channel=REPLACE-ME-WITH-NEW-CHANNEL&autoplay=false&' \
                         'parent=ugprojectsite.herokuapp.com" frameborder="0" allowfullscreen="true" scrolling="no"' \
                         ' height="378" width="620"></iframe>'

    for channelInformation in twitchChannelDetails:

        if channelInformation.get('channelName') is None:
            # If there aren't many streamers for given game (e.g. 'AO TENNIS 2', 'Tiger Woods PGA Tour 2005')
            htmlReturnStringBuilder += 'If you are seeing this, then unfortunately there aren\'t many live ' \
                                       'streamers playing this game at the moment. There should be <strong>three</strong> embedded' \
                                       ' Twitch streams here. If you see less than this number, then the amount of embeds' \
                                       ' you see denotes the amount of live streamers there are for this game on Twitch' \
                                       ' at this time.'

            break
        tempTwitchEmbedDetails = twitchEmbedDetails.replace('REPLACE-ME-WITH-NEW-CHANNEL',
                                                            channelInformation['channelName'])

        htmlReturnStringBuilder += 'Here is a streamer channel named <strong>' + channelInformation['channelDisplayName'] + '</strong> streaming ' + \
                                    nameOfGameThatHasBeenRecommended +' with <strong>' + \
                                   str(channelInformation['currentViewerCount']) + ' viewers</strong> currently watching!' \
                                   ' They are ' + channelInformation['streamType'] +'.<p></p>' \
                                   'The stream\'s title is "<strong>' + channelInformation['streamTitle'] +'</strong>". <p></p><div  class="d-flex justify-content-center">'

        htmlReturnStringBuilder += tempTwitchEmbedDetails
        htmlReturnStringBuilder += '</div><p></p>'

    htmlReturnStringBuilder += '<p class="mb-4 pb-4 border-bottom text-center"></div></div>'
    return htmlReturnStringBuilder


def createYouTubeHTMLCode(htmlReturnStringBuilder, nameOfGameThatHasBeenRecommended):

    htmlReturnStringBuilder += '<H5 class="mb-4 pb-2">Here are the three most relevant videos on <strong>YouTube</strong> for ' \
                               ' <strong style="color:blue">' + nameOfGameThatHasBeenRecommended + '!</strong></h5>' \
                               'The following videos are the top three search results produced ' \
                               'by YouTube if you were to search "' + nameOfGameThatHasBeenRecommended + '". ' \
                               'They are ranked according to what YouTube determines as the most ' \
                               'relevant videos to the search term.<p></p>'

    htmlReturnStringBuilder += '<div class="row"><div class="col-sm">'
    listOfYouTubeVideos = theSite.YouTubeAPI.returnListOfStoredVideos(nameOfGameThatHasBeenRecommended)

    for video in listOfYouTubeVideos:
        htmlReturnStringBuilder += 'The title of this video is "<strong>' + video + '".</strong><p></p><div  class="d-flex justify-content-center">' \
                                   '<iframe width="560" height="315" src= "' + listOfYouTubeVideos.get(video) + '"' \
                                    'frameborder="0" allow="accelerometer; autoplay; clipboard-write;' \
                                    ' encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>' \
                                    '</div><p></p>'


    htmlReturnStringBuilder += '<p class="mb-4 pb-4 border-bottom text-center"></div></div>' # closing div for row col-sm & row
    return htmlReturnStringBuilder


def createIGDBHTMLCode(htmlReturnStringBuilder, nameOfGameForTheRecommendationToBeBasedOffOf, gameIDObject, skipRecommendation):
    igdbHeaders = theSite.views.igdbHeaders

    igdbGameInfoResponseForTheRecommendationToBeBasedOffOfJSON = theSite.IGDBapi.getDetailsAboutGame(nameOfGameForTheRecommendationToBeBasedOffOf,
                                                                                                     igdbHeaders)

    ######################## Recommendation ###########################

    if skipRecommendation is True:
        recommendedGameIgdbBasedJSON = igdbGameInfoResponseForTheRecommendationToBeBasedOffOfJSON
        nameOfGameThatHasBeenRecommended = recommendedGameIgdbBasedJSON[0]['name']
    else:
        listOfGamesForRecommendationAlgorithmToBeRunAgainst = theSite.IGDBapi.getRelatedGamesByGenre(
            igdbGameInfoResponseForTheRecommendationToBeBasedOffOfJSON, igdbHeaders)
        recommendedGameIgdbBasedJSON = theSite.RecommendationAlgorithm.recommendationAlgorithm(igdbGameInfoResponseForTheRecommendationToBeBasedOffOfJSON, listOfGamesForRecommendationAlgorithmToBeRunAgainst)
        recommendedGameIgdbBasedJSON = [recommendedGameIgdbBasedJSON]
        nameOfGameThatHasBeenRecommended = recommendedGameIgdbBasedJSON[0]['name']
    # Debug

    # pprint(recommendedGameIgdbBasedJSON)

    ### GENERATE THIS AFTER RECOMMENDATION HAS BEEN FOUND ###

    igdbCoverImageForGame = theSite.IGDBapi.getCoverImageForGame(recommendedGameIgdbBasedJSON, igdbHeaders, gameIDObject)

    print('RECOMMENDED GAME NAME -------------------> ' + str(nameOfGameThatHasBeenRecommended) + '\n')

    gameIDObject.iGDBName = nameOfGameThatHasBeenRecommended

    # todo add skip recommendation here to modify the recommendation page
    if skipRecommendation is True:
        recommendedGameIs = '<H5 class="mb-4 pb-2"> Here are the details found for <strong style="color:blue">' \
                            '' + nameOfGameThatHasBeenRecommended + '!</strong></H5>'
    else:
        recommendedGameIs = '<H5 class="mb-4 pb-2"> The game recommended based on <strong>' + \
                            nameOfGameForTheRecommendationToBeBasedOffOf \
                            + '</strong> is: <strong style="color:blue">' + nameOfGameThatHasBeenRecommended + \
                            '!</strong></H5>'

    htmlReturnStringBuilder += recommendedGameIs

    htmlCodeForCoverImage = '<div class="row"><img src="' + igdbCoverImageForGame + '"' \
                            'style="width: 150px;height: 200px;" alt="' + nameOfGameForTheRecommendationToBeBasedOffOf \
                            + '">'
    htmlReturnStringBuilder += htmlCodeForCoverImage

    descriptionOfRecommendedGameFromIGDB = recommendedGameIgdbBasedJSON[0]['summary']

    descriptionString = '<div class="col-sm"><p><u>Description:</u></p>' + descriptionOfRecommendedGameFromIGDB

    htmlReturnStringBuilder += descriptionString

    externalURLLinkToIGDB = recommendedGameIgdbBasedJSON[0]['url']

    externalURLLinkString = '<p></p><p>IGDB: <a href="' + externalURLLinkToIGDB + '">' + externalURLLinkToIGDB \
                            + '</a></p></div></div><p class="mb-4 pb-4 border-bottom text-center">'

    htmlReturnStringBuilder += externalURLLinkString

    return htmlReturnStringBuilder