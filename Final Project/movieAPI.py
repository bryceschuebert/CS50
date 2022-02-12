import requests
from keys import RAPIDAPI_HOST, RAPIDAPI_KEY, imdbKey
import json

def get_genres(movie_id):

    url = "https://imdb8.p.rapidapi.com/title/get-genres"

    querystring = {"tconst":movie_id, "format": "json"}

    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
        }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

    return response


def get_movies(movie_title):

    url = f"https://imdb-api.com/en/API/SearchMovie/{imdbKey}/{movie_title}"

    response = requests.request("GET", url).json()

    results = response["results"]
    return results
