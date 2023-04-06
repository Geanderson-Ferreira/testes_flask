import requests
import json

class ApiMovies:
    def __init__(self, search):

        self.TMDB_TOKEN = '&api_key=e2df422e29173e3cd192b7cf3c723365'
        self.API_REQUEST_BASE = 'https://api.themoviedb.org/3'
        self.search = search

    def list_filmes(self):

        query = self.API_REQUEST_BASE + self.search + self.TMDB_TOKEN

        self.response = requests.get(query)

        self.json_file = json.loads(self.response.content)

        return self.json_file





"""
Melhores 2010
/discover/movie?primary_release_year=2010&sort_by=vote_average.desc

Melhores Dramas
/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10



"""
    