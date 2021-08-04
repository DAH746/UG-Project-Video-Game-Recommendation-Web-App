import theSite.tf_idf
import copy
from pprint import pprint

def recommendationAlgorithm(baseGameJSON, listOfGamesToBeCompared):

    previousHighestSimilarityValue = -1  # Initialise 'previous' Similarity value for the loop below

    for game in listOfGamesToBeCompared:

        if baseGameJSON[0]['id'] != game['id']:

            temporaryStorage = []

            textsSimilarityValue = tf_idf_textSimilarityValue(baseGameJSON, game)
            genreSimilarityValue = genreShareCount(baseGameJSON, game)
            gameModeSimilarityValue = gameModeShareCount(baseGameJSON, game)
            sameDeveloperSimilarityValue = doBothGamesShareDevelopers(baseGameJSON, game)
            aggregatedRatingSimilarityValue = ratingValueSimilarity(baseGameJSON, game)

            temporaryStorage.append(textsSimilarityValue)
            temporaryStorage.append(genreSimilarityValue)
            temporaryStorage.append(gameModeSimilarityValue)
            temporaryStorage.append(sameDeveloperSimilarityValue)
            temporaryStorage.append(aggregatedRatingSimilarityValue)

            currentIterationSimilarityValue = finalSimilarityCalculation(temporaryStorage)

            if currentIterationSimilarityValue > previousHighestSimilarityValue:

                previousHighestSimilarityValue = currentIterationSimilarityValue
                currentRecommendedGame = game  # This game is currently the most recommended game

    # Debug
    # print('\n------------------------------------------START: Recommended Game Chosen Info------------------------------------')
    # print('\n Highest Similarity value produced is: ' + str(previousHighestSimilarityValue) + '\n')
    # pprint(currentRecommendedGame)
    # print('\n-----------------------------------------END: Recommended Game Chosen Info-------------------------------------\n')

    return currentRecommendedGame


def finalSimilarityCalculation(temporaryStorage):
    totalValuesInList = len(temporaryStorage)

    sumOfAllValues = 0
    for value in temporaryStorage:
        sumOfAllValues += value

    # Debug

    # print('\nNumerator (sum of all values): ' + str(sumOfAllValues))
    # print('\nDenominator (length of array): ' + str(totalValuesInList))

    finalSimilarityValue = sumOfAllValues / totalValuesInList

    # print('Final Similarity Value: ' + str(finalSimilarityValue))

    return finalSimilarityValue

def tf_idf_textSimilarityValue(baseGameJSON, gameItsBeingComparedToJSON):

    try:
        baseGameDescription = baseGameJSON[0]['summary']
        gameItsBeingComparedToDescription = gameItsBeingComparedToJSON['summary']

        textsSimilarityValue = theSite.tf_idf.tf_idf_function(baseGameDescription, gameItsBeingComparedToDescription)
        # # Debug:
        # print('\nTD-IDF VALUE: ' + str(textsSimilarityValue))
    except KeyError:
        # As if 'summary' is not found, then there is no summary to compare against, therefore 0 for similarity
        return 0

    return textsSimilarityValue


def genreShareCount(baseGameJSON, gameItsBeingComparedToJSON):
    genresOfBaseGame = baseGameJSON[0]['genres']
    genresOfGameItsBeingComparedTo = gameItsBeingComparedToJSON['genres']

    combinedGenres = copy.deepcopy(genresOfBaseGame)
    combinedGenres += genresOfGameItsBeingComparedTo

    sharedGenres = set(genresOfBaseGame) & set(genresOfGameItsBeingComparedTo)
    totalUniqueGenreList = list(set(combinedGenres))

    valueOfSimilarity = len(sharedGenres) / len(totalUniqueGenreList)

    # Debug:
    # print('\nGenres of Base Game: ' + str(genresOfBaseGame))
    # print('\nGenres of comparison Game: ' + str(genresOfGameItsBeingComparedTo))
    # print('\nSet of shared and unique Genres: ' + str(sharedGenres))
    # print('\nGenres shared that are unique: ' + str(totalUniqueGenreList))
    # print('\nCombined Genres: ' + str(combinedGenres))
    #
    # print('\nValue produced from calculation similarity: ' + str(valueOfSimilarity))

    return valueOfSimilarity

def gameModeShareCount(baseGameJSON, gameItsBeingComparedToJSON):

    try:  # If no game modes found, then cannot be similar -> Return 0
        baseGameModes = baseGameJSON[0]['game_modes']
        gameItsBeingComparedToGameModes = gameItsBeingComparedToJSON['game_modes']
    except KeyError as e:
        # print('\n***********Key Error for game_modes: ' + str(e))
        # # Debug
        # print('\nFinal similarity value for Game Mode Shared: 0')
        # # Debug end
        return 0

    # # Debug part 1:
    # print('\nGame modes for base game: ' + str(baseGameModes))
    # print('\nGame modes for Comparison game: ' + str(gameItsBeingComparedToGameModes))

    combinedGameModes = copy.deepcopy(baseGameModes)
    combinedGameModes += gameItsBeingComparedToGameModes

    sharedGameModes = set(baseGameModes) & set(gameItsBeingComparedToGameModes)
    totalUniqueGameModes = list(set(combinedGameModes))

    valueOfSimilarityForGameModes = len(sharedGameModes) / len(totalUniqueGameModes)

    # # Debug part 2:
    # print('\nShared Game modes are (set taken): ' + str(sharedGameModes))
    # print('\nTotal unique game modes (list of a set): ' + str(totalUniqueGameModes))
    # print('\nFinal similarity value: ' + str(valueOfSimilarityForGameModes))

    return valueOfSimilarityForGameModes

def doBothGamesShareDevelopers(baseGameJSON, gameItsBeingComparedToJSON):

    try:
        baseGameDevelopers = baseGameJSON[0]['involved_companies']
        gameItsBeingComparedToDevelopers = gameItsBeingComparedToJSON['involved_companies']
    except KeyError as e:
        # print('\n***********Key Error for involved_companies: ' + str(e))
        # # Debug
        # print('\nFinal similarity for Shared Developers: 0')
        # # Debug end
        return 0

    # # Debug
    # print('\nBase game developers: ' + str(baseGameDevelopers))
    # print('Comparison game\'s developers: ' + str(gameItsBeingComparedToDevelopers))
    # # Debug end

    if baseGameDevelopers == gameItsBeingComparedToDevelopers:
        return 1
    else:
        return 0

def ratingValueSimilarity(baseGameJSON, gameItsBeingComparedToJSON):

    try:
        baseGameAggregatedRating = baseGameJSON[0]['aggregated_rating']  # Aggregated rating is rating based on  external critic scores
        comparisonGameRating = gameItsBeingComparedToJSON['aggregated_rating']
    except KeyError as e:
        # print('\n***********Key Error for aggregated_rating: ' + str(e))
        # # Debug
        # print('\nFinal similarity for aggregated rating: 0')
        # # Debug end
        return 0

    # # Debug
    # print('\nAggregated rating for base game: ' + str(baseGameAggregatedRating))
    # print('\nAggregated rating for comparison game: ' + str(comparisonGameRating))

    smallestValue = min(baseGameAggregatedRating, comparisonGameRating)

    # Below determines which is the smallest so calculation can be done correctly
    if smallestValue == baseGameAggregatedRating:
        similarityValue = ratingValueSimilarityHelperFunction(baseGameAggregatedRating, comparisonGameRating)
        return similarityValue
    else:
        similarityValue = ratingValueSimilarityHelperFunction(comparisonGameRating, baseGameAggregatedRating)
        return similarityValue

def ratingValueSimilarityHelperFunction(smallestValue, largestValue):

    if largestValue == 0:  # Avoid division by 0 error
        return 0

    similarityValue = smallestValue/largestValue
    # # Debug
    # print('\n Similarity value for Aggregated ratings: ' + str(similarityValue))
    return similarityValue