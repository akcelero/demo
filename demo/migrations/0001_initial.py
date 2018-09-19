# Generated by Django 2.1.1 on 2018-09-19 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=150, unique=True)),
                ('Year', models.DecimalField(decimal_places=0, max_digits=4)),
                ('Rated', models.CharField(max_length=100, null=True)),
                ('Released', models.DateField(null=True)),
                ('Runtime', models.CharField(max_length=100, null=True)),
                ('Genre', models.CharField(max_length=100)),
                ('Director', models.CharField(max_length=150)),
                ('Writer', models.CharField(max_length=150)),
                ('Actors', models.CharField(max_length=200)),
                ('Plot', models.TextField(null=True)),
                ('Language', models.CharField(max_length=100)),
                ('Country', models.CharField(max_length=100)),
                ('Awards', models.CharField(max_length=200, null=True)),
                ('Poster', models.URLField(null=True)),
                ('Metascore', models.IntegerField(null=True)),
                ('imdbRating', models.FloatField(null=True)),
                ('imdbVotes', models.IntegerField(null=True)),
                ('imdbID', models.CharField(max_length=100, unique=True)),
                ('Type', models.CharField(max_length=30)),
                ('DVD', models.DateField(null=True)),
                ('BoxOffice', models.CharField(max_length=100, null=True)),
                ('Production', models.CharField(max_length=100, null=True)),
                ('Website', models.URLField(null=True)),
                ('Response', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Source', models.CharField(max_length=100)),
                ('Value', models.CharField(max_length=50)),
                ('Movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Movie')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='Movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Movie'),
        ),
    ]