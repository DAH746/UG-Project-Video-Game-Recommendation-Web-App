# Final Year UG Project - Video Game Recommendation Web Application
_* Please note, API keys have been removed in this repository. You need API keys from Google (for YouTube) and Twitch (for Twitch and Internet Game Database) in order to restore full functionality. Additionally, Steam does not require an API key._

_** Project is currently hosted at https://ugprojectsite.herokuapp.com/_

_*** Video explanation and demonstration of the application is available here: https://www.youtube.com/watch?v=uEGrtIOCTrQ_

This is my final year project, where I developed a web based video game recommendation application using Python and Django. The purpose of the application is to receive an input from the user, which would be any video game name, and return a game that's similar to it, or for more information about the inputted game (depending on which page the input was entered). 

This was achieved by querying IGDB (Internet Game Database) with the input (game name) in order to return additional information about the game to the backend. This is in addition to multiple games that share the inputted game's genre, unless the input is from the “Game Search Page”, where the following steps will be skipped. The last paragraph of this section details the steps behind the “Game Search Page”. Continuing on, using the data obtained from IGDB for the game itself and a list(s) of games that share a genre, the recommendation algorithm calculates a similarity score for each of the returned games with the inputted game using a manual similarity measure. This is where the characteristics of a game are compared, which in this case are: description, genre, category, developers, and external critic review score.

Once the most similar game is calculated, the name of the game is used as a query parameter for IGDB (in order to attain additional information about the game), YouTube, Steam, and Twitch, using their respective “search” endpoints. The data returned is what is then formatted and returned to the front end.  

Lastly, if the user entered the input on the “Game Search Page”, this would be the page where data is returned that is specific to the game entered, then the steps outlined in the paragraph prior would be identical, except the game name would not be from the recommendation generation segment of the application. 

## Project Boot Instructions

Steps required to get the project running:

  1. Navigate to root of the project's directory in the command line
  2. Whilst in the root of the project's directory: 
    	- Install the dependencies from "requirements.txt" first, using command: "pip install -r requirements.txt"
    	- Run the following command: "python manage.py runserver"
  3. Navigate to "http://127.0.0.1:8000/" within your browser to access the application.

Please note, the Twitch embeds will NOT WORK locally as they are tied to the demonstration domain on Heroku (https://ugprojectsite.herokuapp.com/).

## References and Dependencies

Official Bootstrap template "Dashboard" used: https://getbootstrap.com/docs/4.0/examples/dashboard/

Scikit-learn: https://pypi.org/project/scikit-learn/

Requests: https://pypi.org/project/requests/

Pandas: https://pypi.org/project/pandas/

jQuery: https://jquery.com/


