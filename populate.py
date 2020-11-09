import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ukboa_site.settings')

import django
django.setup()


import pandas as pd
import datetime

from front_end.models import Film, Actor, Director, Writer


#################################################################
#################################################################
#######################    GOOD CODE   ##########################
#################################################################
#################################################################

#populate inital actor data table
def add_actor_data():
    actor_film_data = pd.read_csv('/Users/EdmundLudlow/Desktop/Programming/actor_dashboard/Dashboard_Databases/UKBOA_Final_data/actor_data.csv')

    for index, row in actor_film_data.iterrows():
        
        if str(row['Actor ID']) == 'nan':
            actor_id = None
        else:
            actor_id = str(row['Actor ID'])
        
        if str(row['Actor']) == 'nan':
            actor_name = None
        else:
            actor_name = str(row['Actor'])
        
        if str(row['Actor Image']) == 'nan':
            actor_headshot = None
        else:
            actor_headshot = str(row['Actor Image'])

        dob_split = str(row['Date of Birth']).split('-')
        print(dob_split)
        if dob_split[0] =='0':
            dob_split = ['nan']
        if len(dob_split)>2:
            if dob_split[2] == '0'or dob_split[2] == '00':
                dob_split[2] = '1'
            if dob_split[1] == '0'or dob_split[1] == '00':
                dob_split[1] = '1'
        dob_split_join = "-".join(dob_split)

        if dob_split_join == 'nan':
            actor_dob = None
        else:
            actor_dob = datetime.datetime.strptime(dob_split_join, '%Y-%m-%d').date()

        print(actor_dob)
        
        try:
            actor = Actor.objects.get_or_create(
                imdb_id = actor_id,
                name = actor_name,
                dob = actor_dob,
                headshot = actor_headshot)[0]
        except:
            print(row['Actor ID'])
            continue
        print(row)

#populate director data table
def add_director_data():
    director_film_data = pd.read_csv('/Users/EdmundLudlow/Desktop/Programming/actor_dashboard/Dashboard_Databases/UKBOA_Final_data/director_data.csv')
    for index, row in director_film_data.iterrows():
        
        if str(row['Director ID']) == 'nan':
            director_id = None
        else:
            director_id = str(row['Director ID'])
        
        if str(row['Director']) == 'nan':
            director_name = None
        else:
            director_name = str(row['Director'])
        
        if str(row['Director Image']) == 'nan':
            director_headshot = None
        else:
            director_headshot = str(row['Director Image'])

        dob_split = str(row['Date of Birth']).split('-')
        print(dob_split)
        if dob_split[0] =='0':
            dob_split = ['nan']
        if len(dob_split)>2:
            if dob_split[2] == '0'or dob_split[2] == '00':
                dob_split[2] = '1'
            if dob_split[1] == '0'or dob_split[1] == '00':
                dob_split[1] = '1'
        dob_split_join = "-".join(dob_split)

        if dob_split_join == 'nan':
            director_dob = None
        else:
            director_dob = datetime.datetime.strptime(dob_split_join, '%Y-%m-%d').date()
        
        print(director_dob)
        
        try:
            director = Director.objects.get_or_create(
                imdb_id = director_id,
                name = director_name,
                dob = director_dob,
                headshot = director_headshot)[0]
        except:
            print(row['Director ID'])
            continue
        print(row)

#populate writer data table
def add_writer_data():
    writer_film_data = pd.read_csv('/Users/EdmundLudlow/Desktop/Programming/actor_dashboard/Dashboard_Databases/UKBOA_Final_data/writer_data.csv')
    for index, row in writer_film_data.iterrows():
        
        if str(row['Writer ID']) == 'nan':
            writer_id = None
        else:
            writer_id = str(row['Writer ID'])
        
        if str(row['Writer']) == 'nan':
            writer_name = None
        else:
            writer_name = str(row['Writer'])
        
        if str(row['Writer Image']) == 'nan':
            writer_headshot = None
        else:
            writer_headshot = str(row['Writer Image'])

        dob_split = str(row['Date of Birth']).split('-')
        print(dob_split)
        if dob_split[0] =='0':
            dob_split = ['nan']
        if len(dob_split)>2:
            if dob_split[2] == '0'or dob_split[2] == '00':
                dob_split[2] = '1'
            if dob_split[1] == '0'or dob_split[1] == '00':
                dob_split[1] = '1'
        dob_split_join = "-".join(dob_split)

        if dob_split_join == 'nan':
            writer_dob = None
        else:
            writer_dob = datetime.datetime.strptime(dob_split_join, '%Y-%m-%d').date()
        
        print(writer_dob)
        
        try:
            writer = Writer.objects.get_or_create(
                imdb_id = writer_id,
                name = writer_name,
                dob = writer_dob,
                headshot = writer_headshot)[0]
        except:
            print(row['Writer ID'])
            continue
        print(row)

### POPULATE FILM WITHOUT ACTOR JOINS
def populate_film_model():
    df_final_data = pd.read_csv('/Users/EdmundLudlow/Desktop/Programming/actor_dashboard/Dashboard_Databases/UKBOA_Final_data/film_data.csv')
    for index, row in df_final_data.iterrows():

        imdb = str(row['IMDb ID'])
        film = str(row['Film'])

        if str(row['Total Gross to date']) == 'nan':
            gross = None
        else:
            gross = int(round(float(row['Total Gross to date'])))
        
        if str(row['Opening Weekend']) == 'nan':
            openwkd = None
        else:
            openwkd = int(round(float(row['Opening Weekend'])))
        
        if str(row['Screen Average']) == 'nan':
            avg = None
        else:
            avg = int(round(float(row['Screen Average'])))
        
        if str(row['Length of Run']) == 'nan':
            lor = None
        else:
            lor = int(round(float(row['Length of Run'])))
        
        if str(row['Highest Rank']) == 'nan':
            high = None
        else:
            high = int(round(float(row['Highest Rank'])))

        rls = row['Release Date']

        if str(row['Run Time']) == 'nan':
            run_t = None
        else:
            run_t = int(round(float(row['Run Time'])))
        
        if str(row['Poster']) == 'nan':
            post = None
        else:
            post = str(row['Poster'])
        
        if str(row['Rotten Tomatoes Rating']) == 'nan':
            rtr = None
        else:
            rtr = int(round(float(row['Rotten Tomatoes Rating'])))

        film,_ = Film.objects.get_or_create(
        title = film,
        gross = gross,
        opening = openwkd,
        screen_average = avg,
        run_length = lor,
        best_rank = high,
        release_date = rls,
        imdb_id = imdb,
        run_time = run_t,
        poster = post,
        rt = rtr)

def add_actors_to_films():
    actor_film_join_table = pd.read_csv('/Users/EdmundLudlow/Desktop/Programming/actor_dashboard/Dashboard_Databases/UKBOA_Final_data/actor_film_join_table.csv')
    for index, row in actor_film_join_table.iterrows():
        film_imdb_id = str(row['Film IMDb ID'])
        actor_imdb_id = str(row['Actor IMDb ID'])
        try:
            film_instance = Film.objects.get(imdb_id = film_imdb_id)
        except:
            continue
        print(film_instance)
        try:
            film_instance.actors.add(actor_imdb_id)
        except:
            continue

        film_instance.save() 

def add_directors_to_films():
    director_film_join_table = pd.read_csv('/Users/EdmundLudlow/Desktop/Programming/actor_dashboard/Dashboard_Databases/UKBOA_Final_data/director_film_join_table.csv')
    for index, row in director_film_join_table.iterrows():
        film_imdb_id = str(row['Film IMDb ID'])
        director_imdb_id = str(row['Director IMDb ID'])
        try:
            film_instance = Film.objects.get(imdb_id = film_imdb_id)
        except:
            continue
        try:
            film_instance.director.add(director_imdb_id)
        except:
            continue

        film_instance.save() 

def add_writers_to_films():
    writer_film_join_table = pd.read_csv('/Users/EdmundLudlow/Desktop/Programming/actor_dashboard/Dashboard_Databases/UKBOA_Final_data/writer_film_join_table.csv')
    for index, row in writer_film_join_table.iterrows():
        film_imdb_id = str(row['Film IMDb ID'])
        writer_imdb_id = str(row['Writer IMDb ID'])
        try:
            film_instance = Film.objects.get(imdb_id = film_imdb_id)
        except:
            continue
        print(film_instance)
        try:
            film_instance.writers.add(writer_imdb_id)
        except:
            continue

        film_instance.save() 

def add_additional_actor_data():  
    df_actor_info = pd.read_csv('/Users/EdmundLudlow/Desktop/Programming/actor_dashboard/Dashboard_Databases/UKBOA_Final_data/actor_data.csv')
    for index, row in df_actor_info.iterrows():
        actor_id = row['Actor ID']
        film_search = Film.objects.all()
        actor_film_list = Film.objects.filter(actors__imdb_id=str(actor_id))
        actor_model_data = actor_film_list.filter(actors__imdb_id=str(actor_id)).values_list('gross','run_length', 'screen_average', 'opening')
        total_gross = sum(i[0] for i in actor_model_data if i != None)
        try:
            weeks_in_cinema = sum(i[1] for i in actor_model_data if i != None)
        except:
            continue
        career_screen_average = sum(i[2] for i in actor_model_data if i != None)
        try:
            average_return = round(total_gross/len(actor_film_list))
        except:
            continue
        actor_model = Actor.objects.get(imdb_id = str(actor_id))
        actor_model.career_gross = total_gross
        actor_model.average_box_office_return = average_return
        actor_model.career_screen_average = career_screen_average
        actor_model.weeks_at_uk_cinemas = weeks_in_cinema
        actor_model.save()
        print(total_gross)

df_director_info = pd.read_csv('/Users/EdmundLudlow/Desktop/Programming/actor_dashboard/Dashboard_Databases/UKBOA_Final_data/director_data.csv')
def add_additional_director_data():  
    for index, row in df_director_info.iterrows():
        director_id = row['Director ID']
        film_search = Film.objects.all()
        director_film_list = Film.objects.filter(director__imdb_id=str(director_id))
        director_model_data = director_film_list.filter(director__imdb_id=str(director_id)).values_list('gross','run_length', 'screen_average', 'opening')
        total_gross = sum(i[0] for i in director_model_data if i != None)
        try:
            weeks_in_cinema = sum(i[1] for i in director_model_data if i != None)
        except:
            continue
        career_screen_average = sum(i[2] for i in director_model_data if i != None)
        try:
            average_return = round(total_gross/len(director_film_list))
        except:
            continue

        director_model = Director.objects.get(imdb_id = str(director_id))
        director_model.career_gross = total_gross
        director_model.average_box_office_return = average_return
        director_model.career_screen_average = career_screen_average
        director_model.weeks_at_uk_cinemas = weeks_in_cinema
        director_model.save()
        print(total_gross)

def add_additional_writer_data(): 
    df_writer_info = pd.read_csv('/Users/EdmundLudlow/Desktop/Programming/actor_dashboard/Dashboard_Databases/UKBOA_Final_data/writer_data.csv') 
    for index, row in df_writer_info.iterrows():
        writer_id = row['Writer ID']
        film_search = Film.objects.all()
        writer_film_list = Film.objects.filter(writers__imdb_id=str(writer_id))
        writer_model_data = writer_film_list.filter(writers__imdb_id=str(writer_id)).values_list('gross','run_length', 'screen_average', 'opening')
        total_gross = sum(i[0] for i in writer_model_data if i != None)
        try:
            weeks_in_cinema = sum(i[1] for i in writer_model_data if i != None)
        except:
            continue
        career_screen_average = sum(i[2] for i in writer_model_data if i != None)
        try:
            average_return = round(total_gross/len(writer_film_list))
        except:
            continue
        writer_model = Writer.objects.get(imdb_id = str(writer_id))
        writer_model.career_gross = total_gross
        writer_model.average_box_office_return = average_return
        writer_model.career_screen_average = career_screen_average
        writer_model.weeks_at_uk_cinemas = weeks_in_cinema
        writer_model.save()
        print(total_gross)


def calculate_no_of_actor_joins():
    actors_list = Actor.objects.all()
    
    for actor in actors_list:
        actor_model = Actor.objects.get(imdb_id = str(actor))
        actor_film_number = Film.objects.filter(actors__imdb_id=str(actor)).count()
        actor_model.num_of_films = actor_film_number
        actor_model.save()
        print(actor.name)

def calculate_no_of_director_joins():
    directors_list = Director.objects.all()
    
    for director in directors_list:
        director_model = Director.objects.get(imdb_id = str(director))
        director_film_number = Film.objects.filter(director__imdb_id=str(director)).count()
        director_model.num_of_films = director_film_number
        director_model.save()
        print(director.name)

def calculate_no_of_writer_joins():
    writers_list = Writer.objects.all()
    
    for writer in writers_list:
        writer_model = Writer.objects.get(imdb_id = str(writer))
        writer_film_number = Film.objects.filter(writers__imdb_id=str(writer)).count()
        writer_model.num_of_films = writer_film_number
        writer_model.save()
        print(writer.name)


#UPKEEP FUNCTIONS

def delete_model_data():
    talent_list = FilmTalent.objects.all()
    for talent in talent_list:
        talent.delete()

def add_talent_type():
    actors_list = Actor.objects.all()
    for actor in actors_list:
        actor.talent_type = 1
        actor.save()
    print(actor.talent_type)

    directors_list = Director.objects.all()
    for director in directors_list:
        director.talent_type = 2
        director.save()
    print(director.talent_type)

    writers_list = Writer.objects.all()
    for writer in writers_list:
        writer.talent_type = 3
        writer.save()
    print(writer.talent_type)

def populate_annual_bo_returns():
    for year in range(2002,2021):
        print(year)
        films_that_year = Film.objects.filter(release_date__year = year)
        print(films_that_year)
        for films in films_that_year:
            print(films.gross)
            for film_talent in films.writers.all():
                if year == 2002:
                    film_talent.gross_2002 = int(film_talent.gross_2002 or 0) + films.gross
                elif year == 2003:
                    film_talent.gross_2003 = int(film_talent.gross_2003 or 0) + films.gross
                elif year == 2004:
                    film_talent.gross_2004 = int(film_talent.gross_2004 or 0) + films.gross
                elif year == 2005:
                    film_talent.gross_2005 = int(film_talent.gross_2005 or 0) + films.gross                    
                elif year == 2006:
                    film_talent.gross_2006 = int(film_talent.gross_2006 or 0) + films.gross
                elif year == 2007:
                    film_talent.gross_2007 = int(film_talent.gross_2007 or 0) + films.gross
                elif year == 2008:
                    film_talent.gross_2008 = int(film_talent.gross_2008 or 0) + films.gross
                elif year == 2009:
                    film_talent.gross_2009 = int(film_talent.gross_2009 or 0) + films.gross
                elif year == 2010:
                    film_talent.gross_2010 = int(film_talent.gross_2010 or 0) + films.gross
                elif year == 2011:
                    film_talent.gross_2011 = int(film_talent.gross_2011 or 0) + films.gross
                elif year == 2012:
                    film_talent.gross_2012 = int(film_talent.gross_2012 or 0) + films.gross
                elif year == 2013:
                    film_talent.gross_2013 = int(film_talent.gross_2013 or 0) + films.gross
                elif year == 2014:
                    film_talent.gross_2014 = int(film_talent.gross_2014 or 0) + films.gross
                elif year == 2015:
                    film_talent.gross_2015 = int(film_talent.gross_2015 or 0) + films.gross
                elif year == 2016:
                    film_talent.gross_2016 = int(film_talent.gross_2016 or 0) + films.gross
                elif year == 2017:
                    film_talent.gross_2017 = int(film_talent.gross_2017 or 0) + films.gross
                elif year == 2018:
                    film_talent.gross_2018 = int(film_talent.gross_2018 or 0) + films.gross
                elif year == 2019:
                    film_talent.gross_2019 = int(film_talent.gross_2019 or 0) + films.gross
                elif year == 2020:
                    film_talent.gross_2020 = int(film_talent.gross_2020 or 0) + films.gross
                film_talent.save()

def correct_dates():
    

if __name__ == "__main__":
    print("populating") 
    print("populated")
 
