from django.shortcuts import render
from django.db.models import Sum, Q, Count
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
from front_end.models import Film, Actor, Director, Writer
from django.views.generic import View, TemplateView, DetailView, ListView
from itertools import chain
from datetime import date
import collections

################################################################################################
################################################################################################
####################################### HOME PAGE #############################################
################################################################################################
################################################################################################

def error_404_view(request, exception):
    return render(request,'front_end/404.html')


class HomePage(TemplateView):
    template_name = 'front_end/home_page.html'

class AboutTheSite(TemplateView):
    template_name = 'front_end/about_the_site.html'

class AboutMe(TemplateView):
    template_name = 'front_end/about_me.html'

################################################################################################
################################################################################################
####################################### FILM PAGES #############################################
################################################################################################
################################################################################################

class FilmPage(TemplateView):
    template_name = 'front_end/entries/film_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        film_instance = Film.objects.get(imdb_id=kwargs['pk'])

        #Opening Weekend Pie Chart
        if film_instance.opening == film_instance.gross:
            pie_div = None

        elif film_instance.opening:
            labels = ['Opening Weekend','Rest of Run']
            values = [film_instance.opening, (film_instance.gross-film_instance.opening)]
            trace3 = go.Figure(data=[go.Pie(labels=labels, values=values)])
            trace3.update_layout(
                paper_bgcolor='black',
                plot_bgcolor='black',
                title="Percentage of Box Office Gross account by Opening Weekend",
                font=dict(family='Ramabhadra', size=13, color='white')
                )

            pie_div = plot(trace3, auto_open=False, output_type='div')

        else:
            pie_div = None

        film_actors = film_instance.actors.all()
        actor_list = []
        for actor in film_actors:
            actor_data = Actor.objects.get(imdb_id=str(actor))
            actor_list.append(actor_data)

        film_directors = film_instance.director.all()
        director_list = []
        for director in film_directors:
            director_data = Director.objects.get(imdb_id=str(director))
            director_list.append(director_data)

        film_writers = film_instance.writers.all()
        writer_list = []
        for writer in film_writers:
            writer_data = Writer.objects.get(imdb_id=str(writer.imdb_id))
            writer_list.append(writer_data)

        four_dirs = len(director_list) > 3
        four_writers = len(writer_list) > 3

        context.update({
            'film_data': film_instance,
            'actor_data_list': actor_list,
            'director_data_list':director_list,
            'writer_data_list':writer_list,
            'one_director': (film_instance.director.all().count() == 1),
            'one_writer': (film_instance.writers.all().count() == 1),
            'three_directors': (film_instance.director.all().count() > 2),
            'three_writers': (film_instance.writers.all().count() > 2),
            'pie_div': pie_div
        })

        return context

class GeneralFilmsPage(TemplateView):
    template_name = 'front_end/general_overviews/film_overview/films_home.html'

    def get_context_data(self, **kwargs):
        context = super(GeneralFilmsPage, self).get_context_data(**kwargs)

        top_1000_films = Film.objects.all().order_by('-gross')[:1000]
        model_data = top_1000_films.values_list('release_date', 'gross','title')

        x_value_list = []
        y_value_list = []
        z_value_list = []

        for values in model_data:
            x_value_list.append(values[0])
            y_value_list.append(values[1])
            z_value_list.append(values[2])

        trace1 = go.Scatter(x=x_value_list, y=y_value_list, marker={'color': 'red'}, hovertext = z_value_list,
                            mode="markers+text", name='1st Trace')
        data=go.Data([trace1])
        layout=go.Layout(
            yaxis={'title':'Film Gross Earnings'},
            xaxis={'showgrid':False},
            paper_bgcolor='black',
            plot_bgcolor='black',
            title="Top 1000 films at the UK Box Office 2001-2020",
            font=dict(family='Ramabhadra', size=13, color='white'))

        figure=go.Figure(data=data,layout=layout)
        div = plot(figure, auto_open=False, output_type='div')

        #Get back the top 10 annual films from each year
        top_annual_film_dict = {}
        films_by_annual_gross = {}

        for year in range(2002, 2021):
            films_by_annual_gross[year] = 0
            annual_films = Film.objects.filter(release_date__year=f'{year}')
            top_annual_films = annual_films.order_by('-gross')[:10]

            #create top annual film dictionaries
            top_annual_film_dict[year] = top_annual_films

            for films in annual_films:
                films_by_annual_gross[year] += films.gross

            annual_bo_gross = go.Figure(
                data=[
                    go.Bar(
                        name="Yearly Gross at UK Box Office",
                        x=list(films_by_annual_gross.keys()),
                        y=list(films_by_annual_gross.values()),
                    ),
                ],
                layout=go.Layout(
                    title="Cumulative Yearly Takings at UK Box Office 2001-2020 (all films)",
                    yaxis_title="Yearly Cumulative Gross",
                    paper_bgcolor='black',
                    plot_bgcolor='black',
                    font=dict(family='Ramabhadra', size=13, color='white'),
                    xaxis={'showgrid':False},
                )
            )

        annual_bo_gross_div = plot(annual_bo_gross, auto_open=False, output_type='div')

        context.update({
            'graph': div,
            'top_annual_films': top_annual_film_dict,
            'films_by_annual_gross': films_by_annual_gross,
            'annual_bo_gross_div':annual_bo_gross_div,
        })

        return context

################################################################################################
################################################################################################
##################################### ACTOR OVERVIEWS ##########################################
################################################################################################
################################################################################################

class ActorOverview(TemplateView):
    template_name = 'front_end/general_overviews/actor_overview/actor_home.html'

    def get_context_data(self, **kwargs):
        context = super(ActorOverview, self).get_context_data(**kwargs)

        actors_gross = Actor.objects.all().order_by('-career_gross')[0:5]
        actors_bo_length = Actor.objects.all().order_by('-weeks_at_uk_cinemas')[0:5]
        actors_num_films = Actor.objects.all().order_by('-num_of_films')[0:5]

        actor_by_gross_list = []
        actor_by_gross_names = []
        actors_gross_value_set = actors_gross.values_list('name', 'career_gross')

        for actor in actors_gross_value_set:
            actor_by_gross_list.insert(0,actor[0])
            actor_by_gross_names.insert(0,actor[1])

        actor_by_gross_bar = go.Figure(
            data=[
                go.Bar(
                    name="Gross",
                    x= actor_by_gross_names,
                    y= actor_by_gross_list,
                    orientation='h',
                ),
            ],
            layout=go.Layout(
                font=dict(family='Ramabhadra', size=13, color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                title="Top 5 Actors by Gross",
                yaxis={'showgrid':False},
            )
        )

        actor_bo_bar_div = plot(actor_by_gross_bar, auto_open=False, output_type='div')

        actor_by_bol_list = []
        actor_by_bol_names = []
        actors_bol_value_set = actors_bo_length.values_list('name', 'weeks_at_uk_cinemas')

        for actor in actors_bol_value_set:
            actor_by_bol_list.insert(0,actor[0])
            actor_by_bol_names.insert(0,actor[1])

        actor_by_bol_bar = go.Figure(
            data=[
                go.Bar(
                    name="Gross",
                    x= actor_by_bol_names,
                    y= actor_by_bol_list,
                    orientation='h',
                ),
            ],
            layout=go.Layout(
                font=dict(family='Ramabhadra', size=13, color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                title="Top 5 Actors by Length of Time at Box Office",
                yaxis={'showgrid':False},
            )
        )

        actor_by_bol_bar_div = plot(actor_by_bol_bar, auto_open=False, output_type='div')

        actor_film_num_list = []
        actor_film_num_names = []
        actors_film_num_value_set = actors_num_films.values_list('name', 'num_of_films')

        for actor in actors_film_num_value_set:
            actor_film_num_list.insert(0,actor[0])
            actor_film_num_names.insert(0,actor[1])

        actor_by_film_num_bar = go.Figure(
            data=[
                go.Bar(
                    name="Gross",
                    x= actor_film_num_names,
                    y= actor_film_num_list,
                    orientation='h',
                ),
            ],
            layout=go.Layout(
                font=dict(family='Ramabhadra', size=13, color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                title="The 5 Actors by No. of Films",
                yaxis={'showgrid':False},

            )
        )

        actor_by_film_num_bar_div = plot(actor_by_film_num_bar, auto_open=False, output_type='div')

        context.update({
            'actors_2002': Actor.objects.all().order_by('-gross_2002')[0:10],
            'actors_2003': Actor.objects.all().order_by('-gross_2003')[0:10],
            'actors_2004': Actor.objects.all().order_by('-gross_2004')[0:10],
            'actors_2005': Actor.objects.all().order_by('-gross_2005')[0:10],
            'actors_2006': Actor.objects.all().order_by('-gross_2006')[0:10],
            'actors_2007': Actor.objects.all().order_by('-gross_2007')[0:10],
            'actors_2008': Actor.objects.all().order_by('-gross_2008')[0:10],
            'actors_2009': Actor.objects.all().order_by('-gross_2009')[0:10],
            'actors_2010': Actor.objects.all().order_by('-gross_2010')[0:10],
            'actors_2011': Actor.objects.all().order_by('-gross_2011')[0:10],
            'actors_2012': Actor.objects.all().order_by('-gross_2012')[0:10],
            'actors_2013': Actor.objects.all().order_by('-gross_2013')[0:10],
            'actors_2014': Actor.objects.all().order_by('-gross_2014')[0:10],
            'actors_2015': Actor.objects.all().order_by('-gross_2015')[0:10],
            'actors_2016': Actor.objects.all().order_by('-gross_2016')[0:10],
            'actors_2017': Actor.objects.all().order_by('-gross_2017')[0:10],
            'actors_2018': Actor.objects.all().order_by('-gross_2018')[0:10],
            'actors_2019': Actor.objects.all().order_by('-gross_2019')[0:10],
            'actors_2020': Actor.objects.all().order_by('-gross_2020')[0:10],
            'actors_gross': actors_gross,
            'actors_bo_length': actors_bo_length,
            'actors_num_films': actors_num_films,
            'actor_bo_bar_div': actor_bo_bar_div,
            'actor_by_bol_bar_div': actor_by_bol_bar_div,
            'actor_by_film_num_bar_div': actor_by_film_num_bar_div,

        })
        return context

class ActorOverviewTopAtBO(TemplateView):
    template_name = 'front_end/general_overviews/actor_overview/top_100/top_actors_by_bo.html'

    def get_context_data(self, **kwargs):
        context = super(ActorOverviewTopAtBO, self).get_context_data(**kwargs)

        context.update({
            'actors_gross': Actor.objects.all().order_by('-career_gross')[0:100],
        })
        return context

class ActorOverviewLengthAtBO(TemplateView):
    template_name = 'front_end/general_overviews/actor_overview/top_100/top_actors_by_length.html'

    def get_context_data(self, **kwargs):
        context = super(ActorOverviewLengthAtBO, self).get_context_data(**kwargs)

        context.update({
            'actors_bo_length': Actor.objects.all().order_by('-weeks_at_uk_cinemas')[0:100],
            })

        return context

class ActorOverviewNumFilms(TemplateView):
    template_name = 'front_end/general_overviews/actor_overview/top_100/top_actors_by_films.html'

    def get_context_data(self, **kwargs):
        context = super(ActorOverviewNumFilms, self).get_context_data(**kwargs)

        context.update({
            'actors_num_films': Actor.objects.all().order_by('-num_of_films')[0:100],
            })

        return context

################################################################################################
################################################################################################
#################################### DIRECTOR OVERVIEWS ########################################
################################################################################################
################################################################################################

class DirectorOverview(TemplateView):
    template_name = 'front_end/general_overviews/director_overview/director_home.html'

    def get_context_data(self, **kwargs):
        context = super(DirectorOverview, self).get_context_data(**kwargs)

        directors_gross = Director.objects.all().order_by('-career_gross')[0:5]
        directors_bo_length = Director.objects.all().order_by('-weeks_at_uk_cinemas')[0:5]
        directors_num_films = Director.objects.all().order_by('-num_of_films')[0:5]

        director_by_gross_list = []
        director_by_gross_names = []
        director_gross_value_set = directors_gross.values_list('name', 'career_gross')

        for director in director_gross_value_set:
            director_by_gross_list.insert(0,director[0])
            director_by_gross_names.insert(0,director[1])

        director_by_gross_bar = go.Figure(
            data=[
                go.Bar(
                    name="Gross",
                    x= director_by_gross_names,
                    y= director_by_gross_list,
                    orientation='h',
                ),
            ],
            layout=go.Layout(
                font=dict(family='Ramabhadra', size=13, color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                title="Top 5 Directors by Gross",
                yaxis={'showgrid':False},
            )
        )

        director_bo_bar_div = plot(director_by_gross_bar, auto_open=False, output_type='div')

        director_by_bol_list = []
        director_by_bol_names = []
        directors_bol_value_set = directors_bo_length.values_list('name', 'weeks_at_uk_cinemas')

        for director in directors_bol_value_set:
            director_by_bol_list.insert(0,director[0])
            director_by_bol_names.insert(0,director[1])

        director_by_bol_bar = go.Figure(
            data=[
                go.Bar(
                    name="Gross",
                    x= director_by_bol_names,
                    y= director_by_bol_list,
                    orientation='h',
                ),
            ],
            layout=go.Layout(
                font=dict(family='Ramabhadra', size=13, color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                title="Top 5 Directors by Length of Time at Box Office",
                yaxis={'showgrid':False},
            )
        )

        director_by_bol_bar_div = plot(director_by_bol_bar, auto_open=False, output_type='div')

        director_film_num_list = []
        director_film_num_names = []
        directors_film_num_value_set = directors_num_films.values_list('name', 'num_of_films')

        for director in directors_film_num_value_set:
            director_film_num_list.insert(0,director[0])
            director_film_num_names.insert(0,director[1])

        director_by_film_num_bar = go.Figure(
            data=[
                go.Bar(
                    name="Gross",
                    x= director_film_num_names,
                    y= director_film_num_list,
                    orientation='h',
                ),
            ],
            layout=go.Layout(
                font=dict(family='Ramabhadra', size=13, color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                title="The 5 Directors by No. of Films",
                yaxis={'showgrid':False},
            )
        )

        director_by_film_num_bar_div = plot(director_by_film_num_bar, auto_open=False, output_type='div')

        context.update({
            'directors_2002': Director.objects.all().order_by('-gross_2002')[0:10],
            'directors_2003': Director.objects.all().order_by('-gross_2003')[0:10],
            'directors_2004': Director.objects.all().order_by('-gross_2004')[0:10],
            'directors_2005': Director.objects.all().order_by('-gross_2005')[0:10],
            'directors_2006': Director.objects.all().order_by('-gross_2006')[0:10],
            'directors_2007': Director.objects.all().order_by('-gross_2007')[0:10],
            'directors_2008': Director.objects.all().order_by('-gross_2008')[0:10],
            'directors_2009': Director.objects.all().order_by('-gross_2009')[0:10],
            'directors_2010': Director.objects.all().order_by('-gross_2010')[0:10],
            'directors_2011': Director.objects.all().order_by('-gross_2011')[0:10],
            'directors_2012': Director.objects.all().order_by('-gross_2012')[0:10],
            'directors_2013': Director.objects.all().order_by('-gross_2013')[0:10],
            'directors_2014': Director.objects.all().order_by('-gross_2014')[0:10],
            'directors_2015': Director.objects.all().order_by('-gross_2015')[0:10],
            'directors_2016': Director.objects.all().order_by('-gross_2016')[0:10],
            'directors_2017': Director.objects.all().order_by('-gross_2017')[0:10],
            'directors_2018': Director.objects.all().order_by('-gross_2018')[0:10],
            'directors_2019': Director.objects.all().order_by('-gross_2019')[0:10],
            'directors_2020': Director.objects.all().order_by('-gross_2020')[0:10],
            'directors_gross': directors_gross,
            'directors_bo_length': directors_bo_length,
            'directors_num_films': directors_num_films,
            'director_bo_bar_div': director_bo_bar_div,
            'director_by_bol_bar_div': director_by_bol_bar_div,
            'director_by_film_num_bar_div': director_by_film_num_bar_div,

        })
        return context

class DirectorOverviewTopAtBO(TemplateView):
    template_name = 'front_end/general_overviews/director_overview/top_100/top_directors_by_bo.html'

    def get_context_data(self, **kwargs):
        context = super(DirectorOverviewTopAtBO, self).get_context_data(**kwargs)

        context.update({
            'directors_gross': Director.objects.all().order_by('-career_gross')[0:100],
        })
        return context

class DirectorOverviewLengthAtBO(TemplateView):
    template_name = 'front_end/general_overviews/director_overview/top_100/top_directors_by_length.html'

    def get_context_data(self, **kwargs):
        context = super(DirectorOverviewLengthAtBO, self).get_context_data(**kwargs)

        context.update({
            'directors_bo_length': Director.objects.all().order_by('-weeks_at_uk_cinemas')[0:100],
            })

        return context

class DirectorOverviewNumFilms(TemplateView):
    template_name = 'front_end/general_overviews/director_overview/top_100/top_directors_by_films.html'

    def get_context_data(self, **kwargs):
        context = super(DirectorOverviewNumFilms, self).get_context_data(**kwargs)

        context.update({
            'directors_num_films': Director.objects.all().order_by('-num_of_films')[0:100],
            })

        return context

################################################################################################
################################################################################################
#################################### WRITER OVERVIEWS ########################################
################################################################################################
################################################################################################

class WriterOverview(TemplateView):
    template_name = 'front_end/general_overviews/writer_overview/writer_home.html'

    def get_context_data(self, **kwargs):
        context = super(WriterOverview, self).get_context_data(**kwargs)

        writers_gross = Writer.objects.all().order_by('-career_gross')[0:5]
        writers_bo_length = Writer.objects.all().order_by('-weeks_at_uk_cinemas')[0:5]
        writers_num_films = Writer.objects.all().order_by('-num_of_films')[0:5]

        writer_by_gross_list = []
        writer_by_gross_names = []
        writers_gross_value_set = writers_gross.values_list('name', 'career_gross')

        for writer in writers_gross_value_set:
            writer_by_gross_list.insert(0,writer[0])
            writer_by_gross_names.insert(0,writer[1])

        writer_by_gross_bar = go.Figure(
            data=[
                go.Bar(
                    name="Gross",
                    x= writer_by_gross_names,
                    y= writer_by_gross_list,
                    orientation='h',
                ),
            ],
            layout=go.Layout(
                font=dict(family='Ramabhadra', size=13, color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                title="Top 5 Writers by Gross",
                yaxis={'showgrid':False},
            )
        )

        writer_bo_bar_div = plot(writer_by_gross_bar, auto_open=False, output_type='div')

        writer_by_bol_list = []
        writer_by_bol_names = []
        writers_bol_value_set = writers_bo_length.values_list('name', 'weeks_at_uk_cinemas')

        for writer in writers_bol_value_set:
            writer_by_bol_list.insert(0,writer[0])
            writer_by_bol_names.insert(0,writer[1])

        writer_by_bol_bar = go.Figure(
            data=[
                go.Bar(
                    name="Gross",
                    x= writer_by_bol_names,
                    y= writer_by_bol_list,
                    orientation='h',
                ),
            ],
            layout=go.Layout(
                font=dict(family='Ramabhadra', size=13, color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                title="Top 5 Writers by Length of Time at Box Office",
                yaxis={'showgrid':False},
            )
        )

        writer_by_bol_bar_div = plot(writer_by_bol_bar, auto_open=False, output_type='div')

        writer_film_num_list = []
        writer_film_num_names = []
        writers_film_num_value_set = writers_num_films.values_list('name', 'num_of_films')

        for writer in writers_film_num_value_set:
            writer_film_num_list.insert(0,writer[0])
            writer_film_num_names.insert(0,writer[1])

        writer_by_film_num_bar = go.Figure(
            data=[
                go.Bar(
                    name="Gross",
                    x= writer_film_num_names,
                    y= writer_film_num_list,
                    orientation='h',
                ),
            ],
            layout=go.Layout(
                font=dict(family='Ramabhadra', size=13, color='white'),
                paper_bgcolor='black',
                plot_bgcolor='black',
                title="The 5 Writers by No. of Films",
                yaxis={'showgrid':False},
            )
        )

        writer_by_film_num_bar_div = plot(writer_by_film_num_bar, auto_open=False, output_type='div')

        context.update({
            'writers_2002': Writer.objects.all().order_by('-gross_2002')[0:10],
            'writers_2003': Writer.objects.all().order_by('-gross_2003')[0:10],
            'writers_2004': Writer.objects.all().order_by('-gross_2004')[0:10],
            'writers_2005': Writer.objects.all().order_by('-gross_2005')[0:10],
            'writers_2006': Writer.objects.all().order_by('-gross_2006')[0:10],
            'writers_2007': Writer.objects.all().order_by('-gross_2007')[0:10],
            'writers_2008': Writer.objects.all().order_by('-gross_2008')[0:10],
            'writers_2009': Writer.objects.all().order_by('-gross_2009')[0:10],
            'writers_2010': Writer.objects.all().order_by('-gross_2010')[0:10],
            'writers_2011': Writer.objects.all().order_by('-gross_2011')[0:10],
            'writers_2012': Writer.objects.all().order_by('-gross_2012')[0:10],
            'writers_2013': Writer.objects.all().order_by('-gross_2013')[0:10],
            'writers_2014': Writer.objects.all().order_by('-gross_2014')[0:10],
            'writers_2015': Writer.objects.all().order_by('-gross_2015')[0:10],
            'writers_2016': Writer.objects.all().order_by('-gross_2016')[0:10],
            'writers_2017': Writer.objects.all().order_by('-gross_2017')[0:10],
            'writers_2018': Writer.objects.all().order_by('-gross_2018')[0:10],
            'writers_2019': Writer.objects.all().order_by('-gross_2019')[0:10],
            'writers_2020': Writer.objects.all().order_by('-gross_2020')[0:10],
            'writers_gross': writers_gross,
            'writers_bo_length': writers_bo_length,
            'writers_num_films': writers_num_films,
            'writer_bo_bar_div': writer_bo_bar_div,
            'writer_by_bol_bar_div': writer_by_bol_bar_div,
            'writer_by_film_num_bar_div': writer_by_film_num_bar_div,
        })
        return context

class WriterOverviewTopAtBO(TemplateView):
    template_name = 'front_end/general_overviews/writer_overview/top_100/top_writers_by_bo.html'

    def get_context_data(self, **kwargs):
        context = super(WriterOverviewTopAtBO, self).get_context_data(**kwargs)

        context.update({
            'writers_gross': Writer.objects.all().order_by('-career_gross')[0:100],
        })
        return context

class WriterOverviewLengthAtBO(TemplateView):
    template_name = 'front_end/general_overviews/writer_overview/top_100/top_writers_by_length.html'

    def get_context_data(self, **kwargs):
        context = super(WriterOverviewLengthAtBO, self).get_context_data(**kwargs)

        context.update({
            'writers_bo_length': Writer.objects.all().order_by('-weeks_at_uk_cinemas')[0:100],
            })

        return context

class WriterOverviewNumFilms(TemplateView):
    template_name = 'front_end/general_overviews/writer_overview/top_100/top_writers_by_films.html'

    def get_context_data(self, **kwargs):
        context = super(WriterOverviewNumFilms, self).get_context_data(**kwargs)

        context.update({
            'writer_num_films': Writer.objects.all().order_by('-num_of_films')[0:100],
            })

        return context

################################################################################################
################################################################################################
###################################### TALENT PAGES ############################################
################################################################################################
################################################################################################


class ActorPage(TemplateView):
    template_name = 'front_end/entries/actor_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #SEARCH FUNCTION
        #query = request.GET.get("q")

        #GET ACTOR INFO
        actor = Actor.objects.get(imdb_id=kwargs['pk'])
        actor_film_list = Film.objects.filter(actors__imdb_id=str(actor))
        actor_model_data = actor_film_list.filter(actors__imdb_id=str(actor)).values_list('release_date', 'gross','title', 'run_length', 'screen_average', 'opening')

        #GRAPH DATA CALCULATE
        release_date_value_list = []
        gross_value_list = []
        title_value_list = []
        opening_value_list = []

        for values in actor_model_data:
            release_date_value_list.append(values[0])
            gross_value_list.append(values[1])
            title_value_list.append(values[2])
            opening_value_list.append(values[5])

        trace1 = go.Scatter(x=release_date_value_list, y=gross_value_list, marker={'color': 'red'}, hovertext = title_value_list,
                    mode="markers+text", name='1st Trace')
        data=go.Data([trace1])
        layout = go.Layout(
            title="Actor's Films by Total Gross earned at the British Box Office",
            xaxis={'showgrid':False},
            yaxis={'title':'Gross','showgrid':False},
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(family='Ramabhadra', size=13, color='white'),
            )

        figure=go.Figure(data=data,layout=layout)
        scatter_div = plot(figure, auto_open=False, output_type='div')

        ### Bar Chart
        trace2 = go.Figure(
                data=[
                    go.Bar(
                        name="Gross",
                        x=title_value_list,
                        y=gross_value_list,
                    ),
                    go.Bar(
                        name="Opening",
                        x=title_value_list,
                        y=opening_value_list,
                    ),
                ],
                layout=go.Layout(
                    title="Actor's films broken down by Opening Weekend as a propotion of Total Box Office Gross",
                    yaxis_title="Gross/Opening Weekend",
                    barmode='overlay',
                    font=dict(family='Ramabhadra', size=13, color='white'),
                    xaxis={'showgrid':False},
                    paper_bgcolor='black',
                    plot_bgcolor='black',
                )
            )

        bar_div = plot(trace2, auto_open=False, output_type='div')

        context.update({
            'actor_detail': actor,
            #'total_gross': actor_data.average_box_office_return,
            'actor_film_list': actor_film_list,
            #'film_average': actor_data.average_return,
            #'weeks_in_cinema': actor_data.weeks_at_uk_cinemas,
            #'career_screen_average': actor_data.career_screen_average,
            'scatter_div': scatter_div,
            'bar_div': bar_div,
        })
        return context


class DirectorPage(TemplateView):
    template_name = 'front_end/entries/director_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #SEARCH FUNCTION
        #query = request.GET.get("q")

        #GET DIRECTOR INFO
        director = Director.objects.get(imdb_id=kwargs['pk'])
        director_film_list = Film.objects.filter(director__imdb_id=str(director))
        director_model_data = director_film_list.filter(director__imdb_id=str(director)).values_list('release_date', 'gross','title', 'run_length', 'screen_average', 'opening')

        #GRAPH DATA CALCULATE
        release_date_value_list = []
        gross_value_list = []
        title_value_list = []
        opening_value_list = []

        for values in director_model_data:
            release_date_value_list.append(values[0])
            gross_value_list.append(values[1])
            title_value_list.append(values[2])
            opening_value_list.append(values[5])

        trace1 = go.Scatter(x=release_date_value_list, y=gross_value_list, marker={'color': 'red'}, hovertext = title_value_list,
                    mode="markers+text", name='1st Trace')
        data=go.Data([trace1])
        layout=go.Layout(
            title="Director's Films by Total Gross earned at the British Box Office",
            xaxis={'showgrid':False},
            yaxis={'title':'Gross','showgrid':False},
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(family='Ramabhadra', size=13, color='white'),
            )
        figure=go.Figure(data=data,layout=layout)
        scatter_div = plot(figure, auto_open=False, output_type='div')

        ### Bar Chart
        trace2 = go.Figure(
                data=[
                    go.Bar(
                        name="Gross",
                        x=title_value_list,
                        y=gross_value_list,
                    ),
                    go.Bar(
                        name="Opening",
                        x=title_value_list,
                        y=opening_value_list,
                    ),
                ],
                layout=go.Layout(
                    title="Director's films broken down by Opening Weekend as a propotion of Total Box Office Gross",
                    yaxis_title="Gross/Opening Weekend",
                    xaxis={'showgrid':False},
                    barmode='overlay',
                    font=dict(family='Ramabhadra', size=13, color='white'),
                    paper_bgcolor='black',
                    plot_bgcolor='black',
                )
            )

        bar_div = plot(trace2, auto_open=False, output_type='div')

        context.update({
            'director_detail': director,
            #'total_gross': director_data.average_box_office_return,
            'director_film_list': director_film_list,
            #'film_average': director_data.average_return,
            #'weeks_in_cinema': director_data.weeks_at_uk_cinemas,
            #'career_screen_average': director_data.career_screen_average,
            'scatter_div': scatter_div,
            'bar_div':bar_div,
        })
        return context

class WriterPage(TemplateView):
    template_name = 'front_end/entries/writer_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #SEARCH FUNCTION
        #query = request.GET.get("q")

        #GET WRITER INFO
        writer = Writer.objects.get(imdb_id=kwargs['pk'])
        writer_film_list = Film.objects.filter(writers__imdb_id=str(writer))
        writer_model_data = writer_film_list.filter(writers__imdb_id=str(writer)).values_list('release_date', 'gross','title', 'run_length', 'screen_average', 'opening')

        #GRAPH DATA CALCULATE
        release_date_value_list = []
        gross_value_list = []
        title_value_list = []
        opening_value_list = []

        for values in writer_model_data:
            release_date_value_list.append(values[0])
            gross_value_list.append(values[1])
            title_value_list.append(values[2])
            opening_value_list.append(values[5])

        trace1 = go.Scatter(x=release_date_value_list, y=gross_value_list, marker={'color': 'red'}, hovertext = title_value_list,
                    mode="markers+text", name='1st Trace')
        data=go.Data([trace1])
        layout=go.Layout(
            xaxis={'showgrid':False},
            yaxis={'title':'Gross','showgrid':False},
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(family='Ramabhadra', size=13, color='white'),
            )
        figure=go.Figure(data=data,layout=layout)
        scatter_div = plot(figure, auto_open=False, output_type='div')

        ### Bar Chart
        trace2 = go.Figure(
                data=[
                    go.Bar(
                        name="Gross",
                        x=title_value_list,
                        y=gross_value_list,
                    ),
                    go.Bar(
                        name="Opening",
                        x=title_value_list,
                        y=opening_value_list,
                    ),
                ],
                layout=go.Layout(
                    title="Writer's films broken down by Opening Weekend as a propotion of Total Box Office Gross",
                    yaxis_title="Gross/Opening Weekend",
                    barmode='overlay',
                    font=dict(family='Ramabhadra', size=13, color='white'),
                    paper_bgcolor='black',
                    plot_bgcolor='black',
                )
            )

        bar_div = plot(trace2, auto_open=False, output_type='div')

        context.update({
            'writer_detail': writer,
            #'total_gross': writer_data.average_box_office_return,
            'writer_film_list': writer_film_list,
            #'film_average': writer_data.average_return,
            #'weeks_in_cinema': writer_data.weeks_at_uk_cinemas,
            #'career_screen_average': writer_data.career_screen_average,
            'scatter_div': scatter_div,
            'bar_div':bar_div,
        })
        return context

################################################################################################
################################################################################################
#################################### NAVIGATION PAGES ##########################################
################################################################################################
################################################################################################

class SearchResults(ListView):
    template_name = 'front_end/navigation_pages/search_page.html'
    context_object_name = 'query'
    paginate_by = 10

    def get_queryset(self):
        query_param = self.request.GET['q']

        if query_param.count(" ") > 2:
            film_search = Film.objects.filter(Q(title__icontains=query_param)).distinct().order_by('-gross')
            actor_search = Actor.objects.filter(Q(name__icontains=query_param)).distinct().order_by('-career_gross')
            director_search = Director.objects.filter(Q(name__icontains=query_param)).distinct().order_by('-career_gross')
            writer_search = Writer.objects.filter(Q(name__icontains=query_param)).distinct().order_by('-career_gross')
            return_list = list(chain(film_search, actor_search, director_search, writer_search))
        else:
            film_search = Film.objects.filter(Q(title__icontains=query_param)).distinct().order_by('-gross')
            actor_search = Actor.objects.filter(Q(name__icontains=query_param)).distinct().order_by('-career_gross')
            director_search = Director.objects.filter(Q(name__icontains=query_param)).distinct().order_by('-career_gross')
            writer_search = Writer.objects.filter(Q(name__icontains=query_param)).distinct().order_by('-career_gross')
            return_list = list(chain(actor_search, director_search, writer_search, film_search))
        return return_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'q_value': self.request.GET['q'],
        })

        # filter by a variable captured from url, for example
        return context