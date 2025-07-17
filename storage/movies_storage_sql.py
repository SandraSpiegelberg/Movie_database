"""SQL database storage
include CRUD operations using raw SQL queries
"""


import os
from sqlalchemy import create_engine, text
import requests
from dotenv import load_dotenv
from termcolor import colored


load_dotenv()
API_KEY = os.getenv('API_KEY')

API_URL = "http://www.omdbapi.com/?"

DB_URL = "sqlite:///data//movies.db"



# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_image TEXT NOT NULL
        )
    """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as con:
        result = con.execute(
            text("SELECT title, year, rating, poster_image FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}


def add_movie(title):
    """Add a new movie to the database."""

    movies_url = f'{API_URL}apikey={API_KEY}&t={title}'
    res = requests.get(movies_url, timeout=None)
    movie_data = res.json()
    if res.status_code == 200:
        if movie_data['Response'] == 'False':
            print(colored(movie_data['Error'], "red"))
            return
        else:
            movie_title = movie_data['Title']
            movie_year = movie_data['Year']
            movie_rating = movie_data['imdbRating']
            movie_poster = movie_data['Poster']
    else:
        try:
            print(colored(movie_data['Error'], "red"))
        except requests.exceptions.RequestException as req_err:
            print(colored(f"Error: {res.status_code}, {req_err}", "red"))
            return

    with engine.connect() as con:
        try:
            con.execute(text("INSERT INTO movies (title, year, rating, poster_image) VALUES (:title, :year, :rating, :poster_image)"),
                               {"title": movie_title, "year": movie_year, "rating": movie_rating, "poster_image": movie_poster})
            con.commit()
            print(colored(f"Movie '{movie_title}' added successfully.", "green"))
        except Exception as e:
            print(colored(f"Error: {e}", "red"))


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as con:
        try:
            con.execute(text("DELETE FROM movies WHERE title = :title"),
                               {"title": title})
            con.commit()
            print(colored(f"Movie '{title}' deleted successfully.", "green"))
        except Exception as e:
            print(colored(f"Error: {e}", "red"))


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as con:
        try:
            con.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"),
                               {"title": title, "rating": rating})
            con.commit()
            print(colored(f"Movie '{title}' updated successfully.", "green"))
        except Exception as e:
            print(colored(f"Error: {e}", "red"))
