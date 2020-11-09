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
    talent_type = models.IntegerField(blank=True, null=True)
    gross_2002 = models.IntegerField(blank=True, null=True)
    gross_2003 = models.IntegerField(blank=True, null=True)
    gross_2004 = models.IntegerField(blank=True, null=True)
    gross_2005 = models.IntegerField(blank=True, null=True)
    gross_2006 = models.IntegerField(blank=True, null=True)
    gross_2007 = models.IntegerField(blank=True, null=True)
    gross_2008 = models.IntegerField(blank=True, null=True)
    gross_2009 = models.IntegerField(blank=True, null=True)
    gross_2010 = models.IntegerField(blank=True, null=True)
    gross_2011 = models.IntegerField(blank=True, null=True)
    gross_2012 = models.IntegerField(blank=True, null=True)
    gross_2013 = models.IntegerField(blank=True, null=True)
    gross_2014 = models.IntegerField(blank=True, null=True)
    gross_2015 = models.IntegerField(blank=True, null=True)
    gross_2016 = models.IntegerField(blank=True, null=True)
    gross_2017 = models.IntegerField(blank=True, null=True)
    gross_2018 = models.IntegerField(blank=True, null=True)
    gross_2019 = models.IntegerField(blank=True, null=True)
    gross_2020 = models.IntegerField(blank=True, null=True)

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
    talent_type = models.IntegerField(blank=True, null=True)
    gross_2002 = models.IntegerField(blank=True, null=True)
    gross_2003 = models.IntegerField(blank=True, null=True)
    gross_2004 = models.IntegerField(blank=True, null=True)
    gross_2005 = models.IntegerField(blank=True, null=True)
    gross_2006 = models.IntegerField(blank=True, null=True)
    gross_2007 = models.IntegerField(blank=True, null=True)
    gross_2008 = models.IntegerField(blank=True, null=True)
    gross_2009 = models.IntegerField(blank=True, null=True)
    gross_2010 = models.IntegerField(blank=True, null=True)
    gross_2011 = models.IntegerField(blank=True, null=True)
    gross_2012 = models.IntegerField(blank=True, null=True)
    gross_2013 = models.IntegerField(blank=True, null=True)
    gross_2014 = models.IntegerField(blank=True, null=True)
    gross_2015 = models.IntegerField(blank=True, null=True)
    gross_2016 = models.IntegerField(blank=True, null=True)
    gross_2017 = models.IntegerField(blank=True, null=True)
    gross_2018 = models.IntegerField(blank=True, null=True)
    gross_2019 = models.IntegerField(blank=True, null=True)
    gross_2020 = models.IntegerField(blank=True, null=True)

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
    talent_type = models.IntegerField(blank=True, null=True)
    gross_2002 = models.IntegerField(blank=True, null=True)
    gross_2003 = models.IntegerField(blank=True, null=True)
    gross_2004 = models.IntegerField(blank=True, null=True)
    gross_2005 = models.IntegerField(blank=True, null=True)
    gross_2006 = models.IntegerField(blank=True, null=True)
    gross_2007 = models.IntegerField(blank=True, null=True)
    gross_2008 = models.IntegerField(blank=True, null=True)
    gross_2009 = models.IntegerField(blank=True, null=True)
    gross_2010 = models.IntegerField(blank=True, null=True)
    gross_2011 = models.IntegerField(blank=True, null=True)
    gross_2012 = models.IntegerField(blank=True, null=True)
    gross_2013 = models.IntegerField(blank=True, null=True)
    gross_2014 = models.IntegerField(blank=True, null=True)
    gross_2015 = models.IntegerField(blank=True, null=True)
    gross_2016 = models.IntegerField(blank=True, null=True)
    gross_2017 = models.IntegerField(blank=True, null=True)
    gross_2018 = models.IntegerField(blank=True, null=True)
    gross_2019 = models.IntegerField(blank=True, null=True)
    gross_2020 = models.IntegerField(blank=True, null=True)

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
