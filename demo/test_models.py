from django.test import TestCase
from .models import Comment, Movie, Rating
from django.db.utils import IntegrityError


class ModelTestCase(TestCase):

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
            "Poster": "https://m.media-amazon.com/images/M/MV5BMTQwMDU5NDkxNF5\
                BMl5BanBnXkFtZTcwMjk5OTk4OQ@@._V1_SX300.jpg",
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
            k: v for k, v in example_movie_1.items() if k != 'Ratings'}
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
            "Poster": "https://m.media-amazon.com/images/M/MV5BMTQwMDU5NDk\
                xNF5BMl5BanBnXkFtZTcwMjk5OTk4OQ@@._V1_SX300.jpg",
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
            k: v for k, v in example_movie_2.items() if k != 'Ratings'}

    def test_add_movie(self):
        m = Movie(**self.example_movie_no_ratings_1)
        m.save()
        assert(len(Movie.objects.all()) == 1)

    def test_add_movies(self):
        m = Movie(**self.example_movie_no_ratings_1)
        m.save()
        m = Movie(**self.example_movie_no_ratings_2)
        m.save()
        assert(len(Movie.objects.all()) == 2)

    def test_add_existing_movie(self):
        m = Movie(**self.example_movie_no_ratings_1)
        m.save()

        def add_movie():
            m = Movie(**self.example_movie_no_ratings_1)
            m.save()
        self.assertRaises(IntegrityError, add_movie)

    def test_add_movie_with_same_imdbID(self):
        m = Movie(**self.example_movie_no_ratings_1)
        m.save()

        def add_movie():
            same_imdbID = self.example_movie_no_ratings_1
            same_imdbID['imdbID'] = self.example_movie_no_ratings_1['imdbID']
            m = Movie(**same_imdbID)
            m.save()
        self.assertRaises(IntegrityError, add_movie)

    def test_rating(self):
        movie_data = self.example_movie_no_ratings_1
        ratings_data = self.example_movie_1['Ratings']
        movie = Movie(**movie_data)
        movie.save()
        ratings = [
                Rating(Source=r['Source'], Value=r['Value'], Movie=movie)
                for r in ratings_data]
        [r.save() for r in ratings]
        assert(len(Rating.objects.all()) == 3)
        movie.delete()
        movie.save()
        assert(len(Rating.objects.all()) == 0)

    def test_comment(self):
        movie_date = self.example_movie_no_ratings_1
        movie = Movie(**movie_date)
        movie.save()
        Comment(Movie=movie, Text='test').save()
        Comment(Movie=movie, Text='test2').save()
        assert(len(Comment.objects.all()) == 2)
        movie.delete()
        movie.save()
        assert(len(Comment.objects.all()) == 0)
