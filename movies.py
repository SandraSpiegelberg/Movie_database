""" Movie Application
This application allows users to manage their own collection of movies.
Users can add, delete, update, and search for movies,
as well as sorted their collection and view statistics about their collection."""

from statistics import mean, median
import random
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt
from termcolor import colored

import storage.movies_storage_sql as movies_sql


def exit_menu():
    """ Exits the Menu
    :param: None
    :return: None """

    print("Bye!")
    exit()


def command_list_movies():
    """ Lists all the movies in the movies database """
    movies = movies_sql.list_movies()
    total_movies = len(movies)
    print(f"The following {total_movies} movies are in the database: \n")
    for title, value in movies.items():
        print(f"{title} ({value['year']}): {value['rating']}")

    input(colored("Press enter to continue \n", "yellow"))


def command_add_movie():
    """ Adds a movie to the movies database """

    # Get the data from the JSON file
    movies = movies_sql.list_movies()

    title = input("Enter new movie name: ")
    if title in movies:
        print(colored(f"Movie {title} already exist!", "light_red"))

    # Add the movie and save the data to the SQL database
    else:
        try:
            movies_sql.add_movie(title)
        except ValueError as e:
            print(colored(f"Error: {e}", "red"))

    input(colored("Press enter to continue \n", "yellow"))


def command_delete_movie():
    """ Deletes a movie from the movies database """

    movies = movies_sql.list_movies()

    title = input("Enter movie name you want to delete: ")
    if title in movies:
        movies_sql.delete_movie(title)
    else:
        print(colored(f"Movie {title} doesn't exist in the database", "light_red"))

    input(colored("Press enter to continue \n", "yellow"))


def command_update_movie():
    """ Updates the rating of a movie in the movies database """

    movies = movies_sql.list_movies()

    title = input("Enter movie name whose rate you want to update: ")
    if title in movies:
        valid = False
        while not valid:
            rating = input("Enter your rating update between 0-10 : ")
            try:
                rating = float(rating)
                if 0 <= rating <= 10:
                    valid = True
                    movies_sql.update_movie(title, rating)
                else:
                    print(colored("Please enter a rating only between 0-10", "light_red"))
            except ValueError:
                print(colored("Invalid input for rating. Please enter numeric value.", "red"))
    else:
        print(colored(f"Movie {title} doesn't exist in the database", "light_red"))

    input(colored("Press enter to continue \n", "yellow"))


def command_statistics():
    """ Displays statistics about the movies in the database 
    such as average rating (rounded), median rating (rounded), best movie, and worst movie
    if there are multiple movies then print all of them """

    movies = movies_sql.list_movies()
    rating_list = []
    for value_dict in movies.values():
        rating_list.append(value_dict['rating'])
    best_movies = {}
    worst_movies = {}
    try:
        max_rating = max(rating_list)
        min_rating = min(rating_list)
        for movie, value in movies.items():
            if value['rating'] == max_rating:
                best_movies[movie] = value['rating']
            if value['rating'] == min_rating:
                worst_movies[movie] = value['rating']

        stat_dict = {
            'Average rating': round(mean(rating_list), 2),
            'Median rating': round(median(rating_list), 2),
            'Best movies': best_movies,
            'Worst movies': worst_movies
        }

        for key, value in stat_dict.items():
            if not isinstance(value, dict):
                print(f"{key}: {value}")
            else:
                print(f"{key}:")
                for movie, rating in value.items():
                    print(f"{movie}, {rating}")
    except ValueError as e:
        print(colored(f"The movie database is empty, please add first some movies to the database. {e}", "red"))

    input(colored("Press enter to continue \n", "yellow"))


def command_rating_histogram():
    """ Shows a rating histogram of the movies in the database and 
    save the plot in a file if the user want's """

    movies = movies_sql.list_movies()
    rating_list = []
    for value_dict in movies.values():
        rating_list.append(value_dict['rating'])
    print(colored("Close the plot to continue ", "light_red"))
    fig = plt.figure()
    plt.title('The ratings of the movies')
    plt.hist(rating_list)
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.show()

    user_save = input("Want you to save the plot in a file (y/n)? ")
    if user_save == 'y' or user_save.lower() == 'yes':
        fig_name = input("Enter a name of the plot: ")
        fig.savefig(f"{fig_name}.png")
        plt.close()
        input(colored("Press enter to continue \n", "yellow"))
    else:
        input(colored("Press enter to continue \n", "yellow"))

    


def command_random_movie():
    """ Displays a random movie and it's rating from the movies database """

    movies = movies_sql.list_movies()
    try:
        movie_random = random.choice(list(movies))
        rating_random = movies[movie_random]['rating']
        print(colored(
            f"Your movie for today is: {movie_random}, it's rated {rating_random}.", "light_green"))
    except IndexError as e:
        print(colored(f"The movie database is empty, please add first some movies to the database. {e}", "red"))

    input(colored("Press enter to continue \n", "yellow"))


def command_search_movie():
    """ Searches for a movie in the movies database, case insensitive 
    also searches at fuzzy matching and asks the user if they want to add it if not found """

    movies = movies_sql.list_movies()

    user_search = input("Enter part of movie name: ").lower()
    dict_similar_movies = {}

    for movie, value in movies.items():
        fuzzy_ratio = fuzz.token_set_ratio(user_search, movie)
        if user_search in movie.lower():
            print(f"{movie}: {value['rating']}")
        elif fuzzy_ratio >= 80:
            value['fuzzy_ratio'] = fuzzy_ratio
            dict_similar_movies[movie] = value
        else:
            print(colored(f"The movie {user_search} doesn't exist in the database.", "light_red"))
            user_choice_add = input(f"Would you add {user_search} to the database (y/n)? ").lower()
            if user_choice_add == 'y' or user_choice_add == 'yes':
                movies_sql.add_movie(user_search)

    if dict_similar_movies:
        sort_similar_movies = sorted(dict_similar_movies.items(), key=lambda item: (item[1]['fuzzy_ratio'], item[0]) , reverse=True)
        print(colored(f"The movie {user_search} doesn't exist in the database. Did you mean the following?", "light_red"))
        for movie, value in sort_similar_movies:
            print(f"{movie}: {value['rating']}")
        user_choice_add = input(f"Or would you add {user_search} to the database (y/n)? ").lower()
        if user_choice_add == 'y' or user_choice_add == 'yes':
            movies_sql.add_movie(user_search)    

    input(colored("Press enter to continue \n", "yellow"))


def command_sorted_by_rating():
    """ Displays the movies sorted by rating in descending order (best first) 
    and if rating is the same sorted by movie Z-A"""

    movies = movies_sql.list_movies()

    sort_movies = sorted(movies.items(), key=lambda item: (item[1]['rating'], item[0]), reverse=True)
    print("Movies sorted by rating: \n")
    for movie, value in sort_movies:
        print(f"{movie}: {value['rating']}")

    input(colored("Press enter to continue \n", "yellow"))


def command_sorted_by_year():
    """ Displays the movies and year sorted by year, accordingly
    asking the user whether to show latest first or last """

    movies = movies_sql.list_movies()

    user_input = input("Would you like to see the newest movie first? (y/n): ").lower()
    if user_input == 'y' or user_input == 'yes':
        user_reverse = True
    else:
        user_reverse = False

    sort_movies = sorted(movies.items(), key=lambda item: (item[1]['year'], item[0]), reverse=user_reverse)
    print("Movies sorted by year: \n")
    for movie, value in sort_movies:
        print(f"{movie} ({value['year']}): {value['rating']}")

    input(colored("Press enter to continue \n", "yellow"))


def command_filter_by_movies():
    """ Displays the movies by filters minimum rating, start year, and end year
    Enter minimum rating (leave blank for no minimum rating): 8.0
    Enter start year (leave blank for no start year): 2000
    Enter end year (leave blank for no end year):
    Filtered Movies:
    """

    movies = movies_sql.list_movies()
    valid = False
    while not valid:
        min_rate = input("Enter minimum rating (leave blank for no minimum rating): ")
        start_year = input("Enter start year (leave blank for no start year): ")
        end_year = input("Enter end year (leave blank for no end year): ")
        try:
            min_rate = float(min_rate) if min_rate else 0
            start_year = int(start_year) if start_year else 1000
            end_year = int(end_year) if end_year else 3000
            valid = True
        except ValueError as e:
            print(colored(f"Invalid input, please enter numeric values or leave blank. {e}" , "red"))

    filtered_movies = {}
    for movie, value in movies.items():
        if value['rating'] >= min_rate and start_year <= value['year'] <= end_year:
            filtered_movies[movie] = value
    print("Filtered movies: ")
    for movie, value in filtered_movies.items():
        print(f"{movie} ({value['year']}): {value['rating']}")

    input(colored("Press enter to continue \n", "yellow"))


def serialize_movie():
    """ Create a string that includes html list items, 
    the selected informations of all movies
        :return:  string with selected information of all movies
    """

    movies = movies_sql.list_movies()
    html_str = ""
    for movie, value in movies.items():
        year = value['year']
        poster = value['poster']
        html_str += f'''<li>\n
        <div class="movie">\n
            <img class="movie-poster" src={poster} alt="Poster of the movie {movie}" title="{movie}"/>\n
            <div class="movie-title">{movie}</div>\n
            <div class="movie-year">{year}</div>\n
        </div>\n
        </li>\n'''

    return html_str

def command_generate_website():
    """ Generate a HTML page to show the movies from the database with movie picture, name and year.
    """

    html_text = serialize_movie()

    with open('_static/index_template.html', 'r', encoding='utf-8') as movies_temp_html:
        movie_html_text = movies_temp_html.read()

    movie_html_text = movie_html_text.replace(
        '__TEMPLATE_MOVIE_GRID__', html_text)
    movie_html_text = movie_html_text.replace(
        '__TEMPLATE_TITLE__', 'Your Own Movie App')

    with open('index.html', 'w', encoding='utf-8') as movies_html:
        movies_html.write(movie_html_text)

    print(colored("Website was generated successfully. See index.html", "green"))
    input(colored("Press enter to continue \n", "yellow"))


def show_menu_with_input():
    """ Displays the menu and returns the user's choice 
    :param: None
    :return: None """

    print(colored(f"{'*' * 10} Movie Application Menu {'*' * 10}", "light_blue"))
    for key, value in MENU.items():
        print(colored(f"{key}. {value['description']}", "light_blue"))

    # Input Loop
    while True:
        try:
            user_choice = int(input("Enter your choice (0-12): "))
            if user_choice in MENU:
                return MENU[user_choice]['function']
        except ValueError as e:
            print(colored(f"Please enter a valid number (0-12): {e}", "red"))


# Menu dictionary
MENU = {0: {'description': "Exit",
            'function': exit_menu},
        1: {'description': "List movies",
            'function': command_list_movies},
        2: {'description': "Add movie",
            'function': command_add_movie},
        3: {'description': "Delete movie",
            'function': command_delete_movie},
        4: {'description': "Update movie",
            'function': command_update_movie},
        5: {'description': "Show stats",
            'function': command_statistics},
        6: {'description': "Show histogram",
            'function': command_rating_histogram},
        7: {'description': "Random movie",
            'function': command_random_movie},
        8: {'description': "Search movie",
            'function': command_search_movie},
        9: {'description': "Movies sorted by rating",
            'function': command_sorted_by_rating},
        10: {'description': "Movies sorted by year",
             'function': command_sorted_by_year},
        11: {'description': "Filter movies",
             'function': command_filter_by_movies},
        12: {'description': "Generate website",
             'function': command_generate_website}
        }


def main():
    """Main function to run the script
    :param: None
    :return: None
    """

    # The Main Menu loop
    while True:
        choice_function = show_menu_with_input()
        choice_function()


if __name__ == "__main__":
    main()
