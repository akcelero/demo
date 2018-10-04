import requests
from django.test import TestCase
from unittest.mock import patch
from django.http import HttpResponseBadRequest, JsonResponse,\
    HttpResponseNotFound
from django.test import Client
import json
from .models import Comment, Movie
from .views import Comments, Movies


def side_effect(url, params={}):

    with open('movies_json.js') as f:
        movies = json.load(f)

    title = next((v for k, v in params if k == 't'), None)
    content = json.dumps(movies.get(
        title, {"Response": "False", "Error": "Movie not found!"})).encode()
    response = requests.models.Response()
    response._content = content
    return response


@patch('requests.get', side_effect=side_effect)
class ViewsTestCase(TestCase):

    example_movie_1 = {
            "Title": "Test",
            "Year": "2013",
            "Rated": "TV-MA",
            "Released": "2014-04-04",
            "Runtime": "89 min",
            "Genre": "Drama",
            "Director": "Chris Mason Johnson",
            "Writer": "Chris Mason Johnson (screenplay)",
            "Actors": "Scott Marlowe, Matthew Risch, \
                Evan Boomer, Kevin Clarke",
            "Plot": "In 1985, a gay dance understudy hopes for his on-stage \
                chance while fearing the growing AIDS epidemic.",
            "Language": "English, Portuguese, French",
            "Country": "USA",
            "Awards": "3 wins & 3 nominations.",
            "Poster": "https://m.media-amazon.com/images/M/MV5BMTQ\
                wMDU5NDkxNF5BMl5BanBnXkFtZTcwMjk5OTk4OQ@@._V1_SX300.jpg",
            "Ratings": [{
                    "Source": "Internet Movie Database",
                    "Value": "6.2/10"
                }, {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                }, {
                    "Source": "Metacritic",
                    "Value": "70/100"
                }],
            "Metascore": "70",
            "imdbRating": "6.2",
            "imdbVotes": "1335",
            "imdbID": "tt2407380",
            "Type": "movie",
            "DVD": "2014-06-17",
            "BoxOffice": "N/A",
            "Production": "Variance Films",
            "Website": "http://www.testthefilm.com",
            "Response": "True"}
    example_movie_no_ratings_1 = {
            k: v for k, v in example_movie_1.items()
            if k != 'Ratings'
        }
    example_movie_2 = {
            "Title": "Test2",
            "Year": "2013",
            "Rated": "TV-MA",
            "Released": "2014-04-04",
            "Runtime": "89 min",
            "Genre": "Drama",
            "Director": "Chris Mason Johnson",
            "Writer": "Chris Mason Johnson (screenplay)",
            "Actors": "Scott Marlowe, Matthew Risch, Evan Boomer, \
                Kevin Clarke",
            "Plot": "In 1985, a gay dance understudy hopes for his \
                on-stage chance while fearing the growing AIDS epidemic.",
            "Language": "English, Portuguese, French",
            "Country": "USA",
            "Awards": "3 wins & 3 nominations.",
            "Poster": "https://m.media-amazon.com/images/M/MV5BMTQwMDU\
                5NDkxNF5BMl5BanBnXkFtZTcwMjk5OTk4OQ@@._V1_SX300.jpg",
            "Ratings": [{
                    "Source": "Internet Movie Database",
                    "Value": "6.2/10"
                }, {
                    "Source": "Rotten Tomatoes",
                    "Value": "84%"
                }, {
                    "Source": "Metacritic",
                    "Value": "70/100"
                }],
            "Metascore": "70",
            "imdbRating": "6.2",
            "imdbVotes": "1335",
            "imdbID": "tt2407381",
            "Type": "movie",
            "DVD": "2014-06-17",
            "BoxOffice": "N/A",
            "Production": "Variance Films",
            "Website": "http://www.testthefilm.com",
            "Response": "True"}
    example_movie_no_ratings_2 = {
            k: v for k, v in example_movie_2.items()
            if k != 'Ratings'
        }

    def add_movie(self, movie):
        movie = Movie(**movie)
        movie.save()
        return movie.pk

    def test_add_comment(self, requests_mock):
        pk = self.add_movie(self.example_movie_no_ratings_1)
        response = Client().post(
                '/comments', {'MovieID': pk, 'Text': 'example'})
        assert(isinstance(response, JsonResponse))
        assert(len(Comment.objects.all()) == 1)

    def test_add_comment_to_no_existing_movie(self, requests_mock):
        response = Client().post(
                '/comments', {'MovieID': 10, 'Text': 'example'})
        assert(isinstance(response, HttpResponseBadRequest))
        assert(len(Comment.objects.all()) == 0)

    def test_add_comment_with_no_movie(self, requests_mock):
        response = Client().post('/comments', {'Text': 'example'})
        assert(isinstance(response, HttpResponseBadRequest))

    def test_add_comment_with_no_text(self, requests_mock):
        response = Client().post('/comments', {'MovieID': 123})
        assert(isinstance(response, HttpResponseBadRequest))

    def test_fetch_all_comments(self, requests_mock):
        client = Client()
        pk_1 = self.add_movie(self.example_movie_no_ratings_1)
        pk_2 = self.add_movie(self.example_movie_no_ratings_2)

        response = client.post(
                '/comments', {'MovieID': pk_1, 'Text': 'example'})
        assert(isinstance(response, JsonResponse))
        response = client.post(
                '/comments', {'MovieID': pk_2, 'Text': 'example'})
        assert(isinstance(response, JsonResponse))

        response = client.get('/comments')
        assert(len(json.loads(response.content.decode('utf-8'))) == 2)

    def test_fetch_comments_for_one_movie(self, requests_mock):
        client = Client()
        pk_1 = self.add_movie(self.example_movie_no_ratings_1)
        pk_2 = self.add_movie(self.example_movie_no_ratings_2)

        response = client.post(
                '/comments', {'MovieID': pk_1, 'Text': 'example1'})
        assert(isinstance(response, JsonResponse))
        response = client.post(
                '/comments', {'MovieID': pk_2, 'Text': 'example1'})
        assert(isinstance(response, JsonResponse))
        response = client.post(
                '/comments', {'MovieID': pk_2, 'Text': 'example2'})
        assert(isinstance(response, JsonResponse))

        response = client.get('/comments', {'MovieID': pk_2})
        assert(len(json.loads(response.content.decode('utf-8'))) == 2)

    def test_add_movie_with_no_title(self, requests_mock):
        response = Client().post('/movies', {})
        assert(isinstance(response, HttpResponseBadRequest))

    def test_add_movie(self, requests_mock):
        assert(len(Movie.objects.all()) == 0)
        response = Client().post('/movies', {'Title': 'Test'})
        assert(len(Movie.objects.all()) == 1)
        assert(Movie.objects.all()[0].Title == 'Test')

    def test_anti_duplicate(self, requests_mock):
        client = Client()
        assert(len(Movie.objects.all()) == 0)
        client.post('/movies', {'Title': 'Test'})
        assert(len(Movie.objects.all()) == 1)
        client.post('/movies', {'Title': 'Test'})
        assert(len(Movie.objects.all()) == 1)

    def test_with_doesnt_exists_movie(self, requests_mock):
        response = Client().post('/movies', {'Title': 'nodnqwodnqd12dnpno'})
        assert(isinstance(response, HttpResponseNotFound))

    def test_movies_no_filters(self, requests_mock):
        client = Client()
        titles = ['Transformers', 'Zombieland', 'Deadpool']
        [client.post('/movies', {'Title': t}) for t in titles]
        movies = json.loads(client.get('/movies').content.decode('utf-8'))
        assert(len(movies) == 3)

    def test_movies_filter_genre(self, requests_mock):
        client = Client()
        titles = ['Transformers', 'Zombieland', 'Deadpool']
        [client.post('/movies', {'Title': t}) for t in titles]
        movies = json.loads(
                client.get('/movies', {'Genre': 'comedy'})
                      .content.decode('utf-8'))
        assert(len(movies) == 2)

    def test_movies_filter_released(self, requests_mock):
        client = Client()
        titles = ['Transformers', 'Zombieland', 'Deadpool']
        [client.post('/movies', {'Title': t}) for t in titles]
        movies = json.loads(
                client.get('/movies', {'YearFrom': 2008, 'YearTo': 2017})
                      .content.decode('utf-8'))
        assert(len(movies) == 2)

    def test_movies_filter_imdbRating(self, requests_mock):
        client = Client()
        titles = ['Transformers', 'Zombieland', 'Deadpool']
        [client.post('/movies', {'Title': t}) for t in titles]
        movies = json.loads(
                client.get(
                        '/movies',
                        {'imdbRatingFrom': 7.5, 'imdbRatingTo': 7.9}
                      ).content.decode('utf-8'))
        assert(len(movies) == 1)
