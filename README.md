# Movie_database
## About 

This is a Python project in which a sql database is created and it can be shown on an generated HTML page using freely available JSON data via an API from `https://www.omdbapi.com/`. The user can navigate through the menu in the terminal and save an histogramm plot if desired. 

## Installation

To install this project, clone the repository and install the dependencies in requirements.txt using `pip install -r requirements.txt`.
Additional you need to sing in at `https://omdbapi.com/` for a free API key.
Also you have to create a file for enviroment variables `.env` to save there your free API key.

## Usage

To use this project, run the following command - `python movies.py` or `python3 movies.py`. 
At the moment the terminal Menu in blue shows: 

| 0. |    Exit                    | exit the menu
| 1. |    List movies             | list all added movies of the database
| 2. |    Add movie               | entry only the name of a movie to added in the database 
| 3. |    Delete movie            | entry only the name of a movie to deleted from the database
| 4. |    Update movie            | entry the name and rating of a movie to updated the rating in the database
| 5. |    Show stats              | shows average rating, median rating, best and worst movies  
| 6. |    Show histogram          | shows a rating histogram of the movies in the database
| 7. |    Random movie            | shows a random movie and it's rating from the database
| 8. |    Search movie            | searches for a movie by enter a part the name in the movies database using fuzzy matching
| 9. |    Movies sorted by rating | shows the movies sorted by rating in descending order (best first)         
| 10. |   Movies sorted by year   | shows the movies sorted by year, asks the user for the order        
| 11. |   Filter movies           | shows the movies by filters user input of minimum rating, start year, and end year
| 12. |   Generate website        | Generate a HTML page to show the movies from the database with movie picture, name and year.    

If the movies are available in the movie database of `omdbapi.com`. 
If there is an incorrect entry or the movie does not exist in the database, an error message is displayed in red on the terminal and you can re-enter you input again.

## Contributing

If you'd like to contribute to this project, please follow these guidelines:
-   create a new branch to experiment with the code and possibly also open a new issue in case of additional content or wishes
-   if you find something interesting and want to share it, create a pull request
-   in case of bugs or problems, open a new issue and describe the bug/problem and mark it with labels
