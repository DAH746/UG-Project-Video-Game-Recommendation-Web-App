from theSite.views import *
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def tf_idf_function(descriptionGame1, descriptionGame2):

    # # Debug pt1

    # print("\nBEFORE:\n")
    # # The following prints the incoming texts:
    # print("Text 1:\n" + descriptionGame1 + "\n")
    # print("Text 2:\n" + descriptionGame2 + "\n")

    # # Debug END pt1

    # Stop words (common words) are removed:
    vectorizer = TfidfVectorizer(stop_words='english', use_idf=True)  # use_idf is True by default, smooth_idf is true by default

    corpus = [descriptionGame1, descriptionGame2]
    vectors = vectorizer.fit_transform(corpus)

    similarity_matrix = cosine_similarity(vectors)

    # # START - Debug pt2

    # words = vectorizer.get_feature_names()
    # df = pd.DataFrame(vectors.toarray(), columns=words)
    # pd.set_option('display.max_columns', 500)  # Avoids the output: '...' which represents the not showable columns
    #
    # pprint(df) # Prints the data in panda's 'DataFrame' data structure
    # print() # Space prints required because cannot append + "\n" to panda's structures
    # print(words) # All words in 'bag'
    # print()
    # print(similarity_matrix) # Prints value of cosine in matrix form
    # print()

    # # END - Debug pt2

    cosineSimilarityValueBetweenTextsAandB = similarity_matrix[0][1]
    # similarity_matrix (example):
    #
    # [[1.         0.02647118]
    #  [0.02647118 1.]]
    #
    # similarity_matrix[0][1] --> 0.02647118
    textsSimilarityValue = cosineSimilarityValueBetweenTextsAandB  # Code readability purpose

    ##TEST 21/03/2021
    # count_vectorizer = CountVectorizer()
    # vector_matrix = count_vectorizer.fit_transform(data)

    return textsSimilarityValue