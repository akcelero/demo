from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse, \
    HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.forms.models import model_to_dict
import dateparser
import requests
import json
from .models import Movie, Comment, Rating

API_KEY = '744534d'


def get_ratings(movie):
    ratings = Rating.objects.filter(Movie=movie)
    return [{'source': r.Source, 'value': r.Value} for r in ratings]


def serialize_movie(movie):
    fields = [field.name for field in movie._meta.fields if field.name != 'id']
    serialized = model_to_dict(movie, fields=fields)
    serialized['Ratings'] = get_ratings(movie)
    return serialized


def get_movie_by_title_db(title):
    result = Movie.objects.filter(Title=title)
    if result:
        movie = result[0]
        return serialize_movie(movie)
    return None


class Movies(View):
    def post(self, request):
        title = request.POST.get('Title', None)
        if not title:
            return HttpResponseBadRequest('No title in request')

        movie_db = get_movie_by_title_db(title)
        if movie_db:
            return JsonResponse(movie_db)

        params = [('apikey', API_KEY), ('t', title)]
        req = requests.get('http://www.omdbapi.com', params=params)
        data = {k: v if v != 'N/A' else None for k, v in req.json().items()}
        if data.get('Response', None) == 'False':
            return HttpResponseNotFound("Movie with that title doesn't exist")

        movie_db = get_movie_by_title_db(data['Title'])
        if movie_db:
            return JsonResponse(movie_db)

        data.update({k: dateparser.parse(data[k])
                    for k in ['Released', 'DVD']
                    if data[k]})
        data['imdbVotes'] = data['imdbVotes'].replace(',', '')
        ratings_data = data.pop('Ratings')
        movie = Movie(**data)
        movie.save()

        ratings = [
                Rating(Source=r['Source'], Value=r['Value'], Movie=movie)
                for r in ratings_data
            ]
        [r.save() for r in ratings]

        movie_db = get_movie_by_title_db(data['Title'])
        if movie_db:
            return JsonResponse(movie_db)
        return HttpResponseNotFound("Movie with that title doesn't exist")

    def get(self, request):
        filters = {}
        if 'Genre' in request.GET:
            filters.update({'Genre__contains': request.GET.get('Genre', '')})
        if 'Title' in request.GET:
            filters.update({'Title__iexact': request.GET.get('Title', '')})
        if 'Country' in request.GET:
            filters.update({'Country__iexact': request.GET.get('Country', '')})
        if 'Type' in request.GET:
            filters.update({'Type__iexact': request.GET.get('Type', '')})
        if 'YearFrom' in request.GET:
            filters.update({'Year__gte': request.GET.get('YearFrom', 0)})
        if 'YearTo' in request.GET:
            filters.update({'Year__lte': request.GET.get('YearTo', 9999)})
        if 'imdbRatingFrom' in request.GET:
            filters.update({
                'imdbRating__gte': request.GET.get('imdbRatingFrom', 0.0)})
        if 'imdbRatingTo' in request.GET:
            filters.update({
                'imdbRating__lte': request.GET.get('imdbRatingTo', 10.0)})

        result = Movie.objects.filter(**filters)
        movies = [serialize_movie(m) for m in list(result)]
        ratings = list(Rating.objects.all())
        [m.update({'Ratings': {'source': r.Source, 'value': r.Value}})
            for m in movies for r in ratings if r.Movie == m]
        return JsonResponse(movies, safe=False)


class Comments(View):
    def serialize_comment(self, comment):
        return {'MovieID': comment.Movie.pk, 'Text': comment.Text}

    def get(self, request):
        id_ = request.GET.get('MovieID', None)
        if id_:
            result_movies = Movie.objects.filter(pk=id_)
            movie = result_movies[0] if result_movies else None
            comments = Comment.objects.filter(Movie=movie) if movie else []
        else:
            comments = list(Comment.objects.all())

        serializable_comments = [
                self.serialize_comment(c)
                for c in comments
            ] if comments else []
        return JsonResponse(serializable_comments, safe=False)

    def post(self, request):
        id_ = request.POST.get('MovieID', None)
        text = request.POST.get('Text', None)
        if not id_ or not text:
            return HttpResponseBadRequest('No title in request')
        result_movies = Movie.objects.filter(pk=id_)
        if not result_movies:
            return HttpResponseBadRequest('No movie with that id')
        movie = result_movies[0]
        comment = Comment(Movie=movie, Text=text)
        comment.save()

        serializable_comment = self.serialize_comment(comment)
        return JsonResponse(serializable_comment, safe=False)
