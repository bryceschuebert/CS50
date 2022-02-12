import requests

RAPIDAPI_HOST = "imdb8.p.rapidapi.com"
RAPIDAPI_KEY = "ede0a55e89mshfd6588ee5dbdfedp1181b3jsnad2bfe34388d"


def get_genres(movie_id):


    url = "https://imdb8.p.rapidapi.com/title/get-genres"

    querystring = {"tconst":movie_id}

    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text
