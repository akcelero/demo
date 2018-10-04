from django.db import models


class Movie(models.Model):

    Title = models.CharField(max_length=150, unique=True)
    Year = models.DecimalField(max_digits=4, decimal_places=0)
    Rated = models.CharField(max_length=100, null=True)
    Released = models.DateField(null=True)
    Runtime = models.CharField(max_length=100, null=True)
    Genre = models.CharField(max_length=100)
    Director = models.CharField(max_length=150)
    Writer = models.CharField(max_length=150)
    Actors = models.CharField(max_length=200)
    Plot = models.TextField(null=True)
    Language = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    Awards = models.CharField(max_length=200, null=True)
    Poster = models.URLField(null=True)
    Metascore = models.IntegerField(null=True)
    imdbRating = models.FloatField(null=True)
    imdbVotes = models.IntegerField(null=True)
    imdbID = models.CharField(max_length=100, unique=True)
    Type = models.CharField(max_length=30)
    DVD = models.DateField(null=True)
    BoxOffice = models.CharField(max_length=100, null=True)
    Production = models.CharField(max_length=100, null=True)
    Website = models.URLField(null=True)
    Response = models.BooleanField(null=True)

    def __str__(self):
        return self.Title


class Rating(models.Model):
    Source = models.CharField(max_length=100)
    Value = models.CharField(max_length=50)
    Movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s %s)" % (self.Movie.Title, self.Source, self.Value)


class Comment(models.Model):
    Movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    Text = models.TextField()

    def __str__(self):
        return self.Movie.Title[:20] + " - " + self.Text[:30]
