from django.db import models

# Create your models here.

class Actor(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=40)
    dob = models.DateField(blank=True, null=True)
    headshot = models.URLField(max_length=200, blank=True, null=True)
    career_gross = models.IntegerField(blank=True, null=True)
    average_box_office_return = models.IntegerField(blank=True, null=True)
    career_screen_average = models.IntegerField(blank=True, null=True)
    weeks_at_uk_cinemas = models.IntegerField(blank=True, null=True)
    num_of_films = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.imdb_id

class Director(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=40)
    dob = models.DateField(blank=True, null=True)
    headshot = models.URLField(max_length=200, blank=True, null=True)
    career_gross = models.IntegerField(blank=True, null=True)
    average_box_office_return = models.IntegerField(blank=True, null=True)
    career_screen_average = models.IntegerField(blank=True, null=True)
    weeks_at_uk_cinemas = models.IntegerField(blank=True, null=True)
    num_of_films = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.imdb_id

class Writer(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=40)
    dob = models.DateField(blank=True, null=True)
    headshot = models.URLField(max_length=200, blank=True, null=True)
    career_gross = models.IntegerField(blank=True, null=True)
    average_box_office_return = models.IntegerField(blank=True, null=True)
    career_screen_average = models.IntegerField(blank=True, null=True)
    weeks_at_uk_cinemas = models.IntegerField(blank=True, null=True)
    num_of_films = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.imdb_id

class Film(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=60)
    gross = models.IntegerField(blank=True, null=True)
    opening = models.IntegerField(blank=True, null=True)
    screen_average = models.IntegerField(blank=True, null=True)
    run_length = models.IntegerField(blank=True, null=True)
    best_rank = models.IntegerField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    run_time = models.IntegerField(blank=True, null=True)
    poster = models.URLField(max_length=200, blank=True, null=True)
    rt = models.IntegerField(blank=True, null=True)
    actors = models.ManyToManyField(Actor, blank=True, related_name='film_actors')
    director = models.ManyToManyField(Director, blank=True, related_name='film_directors')
    writers = models.ManyToManyField(Writer, blank=True, related_name='film_writers')
