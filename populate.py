import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ukboa_site.settings')

import django
django.setup()

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from dateutil import parser
import json
import os


from front_end.models import Film, Actor, Director, Writer



#########################################
########### FUNCTIONS USED IN ###########
####### MASTER POPULATION SCRIPT ########
#########################################

def database_date_adjuster(unadjusted_date):
    print(type(unadjusted_date))
    if str(type(unadjusted_date)) == "<class 'datetime.date'>" or str(type(unadjusted_date)) == "<class 'datetime.datetime'>":
        return unadjusted_date

    else:
        date_adjuster = unadjusted_date.split('-')
        if date_adjuster[0] =='0':
            date_adjuster = None
        if len(date_adjuster)>2:
            if date_adjuster[2] == '0'or date_adjuster[2] == '00':
                date_adjuster[2] = '1'
            if date_adjuster[1] == '0'or date_adjuster[1] == '00':
                date_adjuster[1] = '1'
        date_adjusted = "-".join(date_adjuster)
        return datetime.strptime(date_adjusted, '%Y-%m-%d').date()

def talent_dob_finder(imdb_talent_soup):
    #Look for talent date of birth in IMDB Soup
    try:
        if len(imdb_talent_soup.findAll('time'))>0:
            for dob_dates in imdb_talent_soup.findAll('time'):
                if dob_dates.has_attr('datetime'):
                    talent_dob_unadjusted = dob_dates['datetime']
                    talent_dob = database_date_adjuster(talent_dob_unadjusted)
                else:
                    talent_dob = None
        else:
            talent_dob = None
    except:
        talent_dob = None

    return talent_dob

def talent_headshot_finder(imdb_talent_soup):
    try:
        talent_data_anchor_tags = imdb_talent_soup.findAll('a')
        talent_data_anchor_tags = list(map(str, talent_data_anchor_tags))
        matching = [s for s in talent_data_anchor_tags if "name-poster" in s]
        if len(matching) > 0:
            photo_available = str(matching[0])
            second_part_string = photo_available[(photo_available.find("src="))+5:]
            talent_image_source = second_part_string[:second_part_string.find('"')]
        else:
            talent_image_source = None
    except:
        talent_image_source = None

    return talent_image_source

def correct_annual_gross(film_year, talent_to_update, film_gross_diff):
    if film_year == 2002:
        talent_to_update.gross_2002 = int(talent_to_update.gross_2002 or 0) + film_gross_diff
    elif film_year == 2003:
        talent_to_update.gross_2003 = int(talent_to_update.gross_2003 or 0) + film_gross_diff
    elif film_year == 2004:
        talent_to_update.gross_2004 = int(talent_to_update.gross_2004 or 0) + film_gross_diff
    elif film_year == 2005:
        talent_to_update.gross_2005 = int(talent_to_update.gross_2005 or 0) + film_gross_diff
    elif film_year == 2006:
        talent_to_update.gross_2006 = int(talent_to_update.gross_2006 or 0) + film_gross_diff
    elif film_year == 2007:
        talent_to_update.gross_2007 = int(talent_to_update.gross_2007 or 0) + film_gross_diff
    elif film_year == 2008:
        talent_to_update.gross_2008 = int(talent_to_update.gross_2008 or 0) + film_gross_diff
    elif film_year == 2009:
        talent_to_update.gross_2009 = int(talent_to_update.gross_2009 or 0) + film_gross_diff
    elif film_year == 2010:
        talent_to_update.gross_2010 = int(talent_to_update.gross_2010 or 0) + film_gross_diff
    elif film_year == 2011:
        talent_to_update.gross_2011 = int(talent_to_update.gross_2011 or 0) + film_gross_diff
    elif film_year == 2012:
        talent_to_update.gross_2012 = int(talent_to_update.gross_2012 or 0) + film_gross_diff
    elif film_year == 2013:
        talent_to_update.gross_2013 = int(talent_to_update.gross_2013 or 0) + film_gross_diff
    elif film_year == 2014:
        talent_to_update.gross_2014 = int(talent_to_update.gross_2014 or 0) + film_gross_diff
    elif film_year == 2015:
        talent_to_update.gross_2015 = int(talent_to_update.gross_2015 or 0) + film_gross_diff
    elif film_year == 2016:
        talent_to_update.gross_2016 = int(talent_to_update.gross_2016 or 0) + film_gross_diff
    elif film_year == 2017:
        talent_to_update.gross_2017 = int(talent_to_update.gross_2017 or 0) + film_gross_diff
    elif film_year == 2018:
        talent_to_update.gross_2018 = int(talent_to_update.gross_2018 or 0) + film_gross_diff
    elif film_year == 2019:
        talent_to_update.gross_2019 = int(talent_to_update.gross_2019 or 0) + film_gross_diff
    elif film_year == 2020:
        talent_to_update.gross_2020 = int(talent_to_update.gross_2020 or 0) + film_gross_diff
    return(talent_to_update)

'''
def find_correct_uk_date(film_id):

    soupified_page = bs(requests.get(f'https://www.imdb.com/title/{film_id}/releaseinfo').text, 'html.parser')
    release_date_table = soupified_page.find('table', {'class': 'release-dates-table-test-only'})

    dates = release_date_table.find_all('td', class_='release-date-item__date')
    countries = release_date_table.find_all('td', class_='release-date-item__country-name')

    secondary_uk_dates = []
    date_count = 0
    for i in range(len(dates)):
        date_count += 1
        #Remove additional UK dates
        #Create a list of index positions for UK release dates
        if countries[i].text.strip() == "UK":
            secondary_uk_dates.append(date_count-1)

    if len(secondary_uk_dates) > 1:
        #Remove actual release date
        secondary_uk_dates = secondary_uk_dates[1:]

        #Loop through remaining index positions to remove from dates and countries list
        for index in sorted(secondary_uk_dates, reverse=True):
            del dates[index]
            del countries[index]

    #Run all remaining dates through a loop to input into a dictionary
    dates_as_dic = {}
    for i in range(len(dates)):
        dates_as_dic[countries[i].text.strip()] = dates[i].text

    if dates_as_dic.get('UK'):
        release_date = dates_as_dic.get('UK')
    else:
        release_date = next(iter(dates_as_dic.values()))

    if str(release_date) != 'None':
        if len(release_date.split()) == 3:
            release_datetime = parser.parse(release_date).strftime('%Y-%m-%d')
        elif len(release_date.split()) == 2:
            release_datetime = parser.parse(release_date).strftime('%Y-%m-01')
        elif len(release_date.split()) == 1:
            release_datetime = parser.parse(release_date).strftime('%Y-01-01')
    else:
        release_datetime = parser.parse(release_date).strftime('2001-01-01')

    return release_datetime
'''

def set_column_index(dataframe, header_row):
        new_header = dataframe.iloc[header_row]
        dataframe = dataframe[header_row+1:]
        dataframe.columns = new_header
        return dataframe


#########################################
####### MASTER POPULATION SCRIPT ########
#########################################


def populate_recent_data():

    #Global variables
    SSID = '6cf99b5e'
    INPUT_DIRECTORY = '/home/edmundludlow/UKBOA_Website/bfi_spreadsheets_store/spreadsheet_holding_space/'
    MATCHES = ["(THEATRE)", "(BALLET)", "(CONCERT)", "(EXHIBITION)", "4K RESTORATION", "(RE:", "ANNIVERSARY)"]

    for xls_file in os.listdir(INPUT_DIRECTORY):

        if str(xls_file) == '.DS_Store':
            continue
        else:
            dfs_bfi_spreadsheet = pd.read_excel(INPUT_DIRECTORY + xls_file, header = None)

        print(xls_file)

        #Format dataframes
        #Correct column index line
        if 'Rank' in dfs_bfi_spreadsheet.columns:
                continue
        else:
            #Find the row with the desired header
            index_row = dfs_bfi_spreadsheet.index[dfs_bfi_spreadsheet.iloc[:,0] == 'Rank'].tolist()
            #Move Header row to index
            dfs_bfi_spreadsheet = set_column_index(dfs_bfi_spreadsheet, index_row[0])

        dfs_bfi_spreadsheet.dropna(subset = ['Rank', 'Total Gross to date'], inplace=True)

        for index, row in dfs_bfi_spreadsheet.iterrows():

            #Set up variables
            title = row['Film'].upper()

            #Check for Harry Potter

            if "HARRY POTTER" in str(title):
                title_list = title.upper().replace('AND', '&')
                title = str(title_list).split("&")[1]

            elif any(x in title for x in MATCHES):
                continue

            title_formatted = title.lower().replace(' ', '_')

            #Look for the release date given in dataframe
            r = requests.get(f'http://www.omdbapi.com/?apikey={SSID}&t={title_formatted}&type=movie')
            data = json.loads(r.text)

            #Check for error messages and try another method if we get one
            if len(data) < 5:
                title_and_replaced = title_formatted.lower().replace('and', '&')
                r = requests.get(f'http://www.omdbapi.com/?apikey={SSID}&t={title_and_replaced}&type=movie')
                data = json.loads(r.text)
                if len(data) < 5:
                    data = False

            if not data:
                #try:
                if Film.objects.filter(title = str(title)).exists():
                    existing_film = Film.objects.get(title = str(title))
                else:
                    continue

            else:
                #set up variables
                imdb_id = str(data['imdbID'])

                if Film.objects.filter(title = str(title)).exists():
                    existing_film = Film.objects.get(title = str(title))
                elif Film.objects.filter(imdb_id = imdb_id).exists():
                    existing_film = Film.objects.get(imdb_id = imdb_id)
                else:
                    existing_film = False


            if existing_film:
                print(existing_film.title)

                if existing_film.release_date == None:
                    year_of_release = int(data['Year'])
                    existing_film.release_date = datetime.strptime(f'{year_of_release}-01-01','%Y-%m-%d')

                #set up global variables
                film_year = existing_film.release_date.year

                #Update run length avoiding re-release info
                if int(row['Weeks on release']) < 20:
                    run_length_diff = int(row['Weeks on release']) - int(existing_film.run_length)
                    if run_length_diff > 0:
                        existing_film.run_length += run_length_diff
                    else:
                        run_length_diff = int(row['Weeks on release'])
                        existing_film.run_length += int(row['Weeks on release'])
                else:
                    run_length_diff = 0

                #Update Film Gross
                film_gross_diff = int(row['Total Gross to date']) - int(existing_film.gross)
                #Filter out data which subtracts from previously inputted columns
                if film_gross_diff < 0:
                    #print(existing_film.title)
                    film_gross_diff = 0

                else:
                    existing_film.gross = int(row['Total Gross to date'])
                    existing_film.screen_average = round((int(existing_film.screen_average) + int(row['Site average']))/2)

                ########################################################################################
                ################################## EXISTING ACTORS #####################################
                ########################################################################################

                #update actor instances with new career gross data
                for actors in existing_film.actors.all():
                    actor_to_update = Actor.objects.get(imdb_id = actors.imdb_id)
                    if actor_to_update.career_gross == None:
                        actor_to_update.career_gross = 0
                    actor_to_update.career_gross += film_gross_diff

                    #Calculate updated actor bo avg.
                    actor_film_list = Film.objects.filter(actors__imdb_id=str(actors.imdb_id))
                    average_return = round(actor_to_update.career_gross/len(actor_film_list))
                    actor_to_update.average_box_office_return = average_return

                    #Calculate updated actor time spent at bo
                    if actor_to_update.weeks_at_uk_cinemas == None:
                        actor_to_update.weeks_at_uk_cinemas = 0
                    actor_to_update.weeks_at_uk_cinemas += run_length_diff

                    actor_to_update = correct_annual_gross(film_year, actor_to_update,film_gross_diff)
                    actor_to_update.save()

                ########################################################################################
                ################################ EXISTING DIRECTORS ####################################
                ########################################################################################

                #update director instances with new career gross data
                for director in existing_film.director.all():

                    director_to_update = Director.objects.get(imdb_id = director.imdb_id)

                    if director_to_update.career_gross == None:
                        director_to_update.career_gross = 0
                    director_to_update.career_gross += film_gross_diff

                    #Calculate updated director bo avg.

                    director_film_list = Film.objects.filter(director__imdb_id=str(director.imdb_id))
                    average_return = round(director_to_update.career_gross/len(director_film_list))
                    director_to_update.average_box_office_return = average_return

                    #Calculate updated director time spent at bo
                    if director_to_update.weeks_at_uk_cinemas == None:
                        director_to_update.weeks_at_uk_cinemas = 0
                    director_to_update.weeks_at_uk_cinemas += run_length_diff

                    director_to_update = correct_annual_gross(film_year, director_to_update,film_gross_diff)

                    director_to_update.save()

                ########################################################################################
                ################################## EXISTING WRITERS ####################################
                ########################################################################################

                for writer in existing_film.writers.all():

                    writer_to_update = Writer.objects.get(imdb_id = writer.imdb_id)

                    if writer_to_update.career_gross == None:
                        writer_to_update.career_gross = 0
                    writer_to_update.career_gross += film_gross_diff

                    #Calculate updated writer bo avg.
                    writer_film_list = Film.objects.filter(writers__imdb_id=str(writer.imdb_id))
                    average_return = round(writer_to_update.career_gross/len(writer_film_list))
                    writer_to_update.average_box_office_return = average_return

                    #Calculate updated actor time spent at bo
                    if writer_to_update.weeks_at_uk_cinemas == None:
                        writer_to_update.weeks_at_uk_cinemas = 0
                    writer_to_update.weeks_at_uk_cinemas += run_length_diff

                    writer_to_update = correct_annual_gross(film_year, writer_to_update,film_gross_diff)

                    writer_to_update.save()
                existing_film.save()

            else:
                if not data:
                    continue
                else:
                    if int(data['Year']) < 2001:
                        continue
                    else:
                        xls_file_split = xls_file.split(":")[1].split("_")

                        xls_file_date = xls_file_split[1].split("-")[0]
                        xls_file_month = xls_file_split[2]
                        xls_file_year = xls_file_split[3]

                        xls_date = xls_file_year + "-" + str(xls_file_month) + "-" + xls_file_date

                        xls_date_corrected = datetime.strptime(xls_date, '%Y-%B-%d').date()

                        if int(row['Weeks on release']) == 1:
                            release_date = xls_date_corrected
                        else:
                            year_of_release = int(data['Year'])
                            release_date = datetime.strptime(f'{year_of_release}-01-01','%Y-%m-%d')

                        release_year = str(release_date)[0:4]

                        if int(release_year) < 2000:
                            continue

                        #Firstly we for new entries we need to fill empty actor, director and writer entries
                        imdb_search_soup = bs(requests.get(f'https://www.imdb.com/title/{imdb_id}').text, 'lxml')

                        ######################################################################################
                        ################################### NEW ACTORS #######################################
                        ######################################################################################

                        #find actors which don't exist in db
                        imdb_actor_search_soup = imdb_search_soup.find('table', {'class': 'cast_list'})

                        try:
                            #This sometimes throws an error if no actors are found on film entry page
                            actor_join_anchor_tags = imdb_actor_search_soup.findAll('a')
                        except:
                            continue

                        actors_to_add = []
                        new_actors_to_create = []

                        for actor_join_tags in actor_join_anchor_tags:
                            #Removes doubling up of anchor tags - each actor is referenced twice on the page
                            if 'characters' in str(actor_join_tags):
                                continue
                            else:
                                actor_id = (str(actor_join_tags).split('/'))[2]
                                actors_to_add.append(actor_id)

                                if Actor.objects.filter(imdb_id = actor_id).exists():
                                    continue
                                else:
                                    new_actors_to_create.append(actor_id)

                        actors_to_add = list(set(actors_to_add))
                        new_actors_to_create = list(set(new_actors_to_create))

                        #for the actors which don't exist in db we need to find initial data to add to our db
                        for actor_id in new_actors_to_create:
                            imdb_actor_data_soup = bs(requests.get(f'https://www.imdb.com/name/{actor_id}').text, 'lxml').find('table')

                            #Look for name in IMDb soup
                            actor_name = imdb_actor_data_soup.find_all('span', {'class' : 'itemprop'})[0].text

                            #Look for actor date of birth in IMDB Soup
                            actor_dob = talent_dob_finder(imdb_actor_data_soup)
                            if len(str(actor_dob)) < 5:
                                actor_dob = None

                            #Look for actor images in IMDB Soup
                            actor_headshot = talent_headshot_finder(imdb_actor_data_soup)

                            new_actor = Actor.objects.create(
                                    imdb_id = actor_id,
                                    name = actor_name,
                                    dob = actor_dob,
                                    headshot = actor_headshot,
                                    talent_type = 1,
                                    career_gross = row['Total Gross to date'],
                                    average_box_office_return = row['Total Gross to date'],
                                    weeks_at_uk_cinemas = int(row['Weeks on release']),
                                    num_of_films = 1)

                            new_actor.save()

                            new_actor_to_update = Actor.objects.get(imdb_id = actor_id)

                            new_actor_to_update = correct_annual_gross(release_date, new_actor_to_update, row['Total Gross to date'])

                            new_actor_to_update.save()

                        ########################################################################################
                        ################################### NEW DIRECTORS ########################################
                        ########################################################################################

                        #find directors which don't exist in db
                        imdb_director_search_soup = imdb_search_soup.find('div', {'class':'credit_summary_item'})

                        try:
                            director_join_anchor_tags = imdb_director_search_soup.findAll('a')
                        except:
                            continue

                        directors_to_add = []
                        new_directors_to_create = []

                        for director_join_tags in director_join_anchor_tags:
                            #Removes doubling up of anchor tags - each actor is referenced twice on the page
                            if len(str(director_join_tags)) > 100:
                                continue
                            else:
                                #director_name = director_join_tags.text
                                director_id = (str(director_join_tags).split('/'))[2]
                                directors_to_add.append(director_id)

                                if not Director.objects.filter(imdb_id = director_id).exists():
                                    new_directors_to_create.append(director_id)

                        directors_to_add = list(set(directors_to_add))
                        new_directors_to_create = list(set(new_directors_to_create))

                        #for the directors which don't exist in db we need to find initial data to add to our db
                        for director_id in new_directors_to_create:
                            imdb_director_data_soup = bs(requests.get(f'https://www.imdb.com/name/{director_id}').text, 'lxml').find('table')

                            #Look for name in IMDb soup
                            director_name = imdb_director_data_soup.find_all('span', {'class' : 'itemprop'})[0].text

                            #Look for director date of birth in IMDB Soup
                            director_dob = talent_dob_finder(imdb_director_data_soup)
                            if len(str(director_dob)) < 5:
                                director_dob = None

                            #Look for headshots in IMDb soup
                            director_headshot = talent_headshot_finder(imdb_director_data_soup)

                            new_director = Director.objects.create(
                                imdb_id = director_id,
                                name = director_name,
                                dob = director_dob,
                                headshot = director_headshot,
                                talent_type = 2,
                                career_gross = row['Total Gross to date'],
                                average_box_office_return = row['Total Gross to date'],
                                weeks_at_uk_cinemas = int(row['Weeks on release']),
                                num_of_films = 1)

                            new_director.save()

                            new_director_to_update = Director.objects.get(imdb_id = director_id)

                            new_director_to_update = correct_annual_gross(release_date, new_director_to_update, row['Total Gross to date'])

                            new_director_to_update.save()

                        ########################################################################################
                        ################################### NEW WRITERS ########################################
                        ########################################################################################
                        imdb_writer_search_soup_unedited = bs(requests.get(f'https://www.imdb.com/title/{imdb_id}/fullcredits/').text, 'lxml').findAll('table', {'class':'simpleTable'})
                        if len(imdb_writer_search_soup_unedited) < 2:
                            continue
                        else:
                            imdb_writer_search_soup = imdb_writer_search_soup_unedited[1]

                        writer_join_anchor_tags = imdb_writer_search_soup.findAll('a')

                        writers_to_add = []
                        new_writers_to_create = []

                        for writer_join_tags in writer_join_anchor_tags:
                            #Removes doubling up of anchor tags - each writer is referenced twice on the page
                            if len(str(writer_join_tags)) > 100:
                                continue
                            else:
                                writer_id = (str(writer_join_tags).split('/'))[2]
                                writers_to_add.append(writer_id)

                                if not Writer.objects.filter(imdb_id = writer_id).exists():
                                    new_writers_to_create.append(writer_id)

                        writers_to_add = list(set(writers_to_add))
                        new_writers_to_create = list(set(new_writers_to_create))

                        print(new_writers_to_create)
                        #for the wrkters which don't exist in db we need to find initial data to add to our db
                        for writer_id in new_writers_to_create:
                            print(writer_id)
                            imdb_writer_data_soup = bs(requests.get(f'https://www.imdb.com/name/{writer_id}').text, 'lxml').find('table')

                            #Look for name in IMDb soup
                            writer_name = imdb_writer_data_soup.find_all('span', {'class' : 'itemprop'})[0].text
                            print(writer_name)

                            #Look for director date of birth in IMDB Soup
                            writer_dob = talent_dob_finder(imdb_writer_data_soup)
                            if len(str(writer_dob)) < 5:
                                writer_dob = None

                            #Look for headshots in IMDb soup
                            writer_headshot = talent_headshot_finder(imdb_writer_data_soup)

                            new_writer = Writer.objects.create(
                                imdb_id = writer_id,
                                name = writer_name,
                                dob = writer_dob,
                                headshot = writer_headshot,
                                talent_type = 3,
                                career_gross = row['Total Gross to date'],
                                average_box_office_return = row['Total Gross to date'],
                                weeks_at_uk_cinemas = int(row['Weeks on release']),
                                num_of_films = 1)

                            new_writer.save()

                            new_writer_to_update = Writer.objects.get(imdb_id = writer_id)

                            new_writer_to_update = correct_annual_gross(release_date, new_writer_to_update, row['Total Gross to date'])

                            new_writer_to_update.save()

                    if str(row['Weeks on release']) == '1':
                        new_film_opening = row['Weekend Gross']
                    else:
                        new_film_opening = None

                    try:
                        new_film_run_time = int(str(data['Runtime']).replace('min',''))
                    except:
                        new_film_run_time = None

                    try:
                        new_film_rt_rating = int(((str(data['Ratings'][1]['Value'])).split('/'))[0])
                    except:
                        new_film_rt_rating = None

                    if release_date != None:
                        adjusted_release_date = database_date_adjuster(release_date)
                    else:
                        adjusted_release_date = release_date


                    new_film = Film.objects.create(
                        imdb_id = str(data['imdbID']),
                        title = str(row['Film']).upper(),
                        gross = str(row['Total Gross to date']),
                        opening = new_film_opening,
                        screen_average = int(row['Site average']),
                        run_length = int(row['Weeks on release']),
                        best_rank = 0,
                        release_date = adjusted_release_date,
                        run_time = new_film_run_time,
                        poster = str(data['Poster']),
                        rt = new_film_rt_rating,
                        )

                    new_film.save()

                    print(new_film.gross)

                    new_film_instance = Film.objects.get(imdb_id=imdb_id)

                    for actor_id in actors_to_add:
                        new_film_instance.actors.add(actor_id)
                    for director_id in directors_to_add:
                        new_film_instance.director.add(director_id)
                    for writer_id in writers_to_add:
                        new_film_instance.writers.add(writer_id)

                    print('at the end')

                    new_film_instance.save()


if __name__ == "__main__":
    print("populating")
    populate_recent_data()
    print("populated")




