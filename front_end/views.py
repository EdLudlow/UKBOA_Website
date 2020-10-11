from django.shortcuts import render
from django.db.models import Sum, Q, Count
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
from front_end.models import Film, Actor, Director, Writer
from django.views.generic import View, TemplateView, DetailView, ListView
from itertools import chain
from datetime import date


# Create your views here.
class HomePage(TemplateView):
    template_name = 'front_end/home_page.html'

class FilmPage(TemplateView):
    template_name = 'front_end/film_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        film_instance = Film.objects.get(imdb_id=kwargs['pk'])

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
        })

        return context

class GeneralFilmsPage(TemplateView):
    template_name = 'front_end/general_films_page.html'

    def get_context_data(self, **kwargs):
        context = super(GeneralFilmsPage, self).get_context_data(**kwargs)

        model_data = Film.objects.values_list('release_date', 'gross','title')
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
        layout=go.Layout(title="Films by Gross", xaxis= {'title':'Year'}, yaxis={'title':'Gross'})
        figure=go.Figure(data=data,layout=layout)
        div = plot(figure, auto_open=False, output_type='div')

        context['graph'] = div

        return context

class ActorOverview(TemplateView):
    template_name = 'front_end/actor_overview.html'

    def get_context_data(self, **kwargs):
        context = super(ActorOverview, self).get_context_data(**kwargs)

        #multiple_films = Film.objects.annotate(count=Count('film_actors').filter(count__gt=5))

        context.update({
            'actors_gross': Actor.objects.all().order_by('-career_gross')[0:5],
            'actors_bo_length': Actor.objects.all().order_by('-weeks_at_uk_cinemas')[0:5],
            'actors_num_films': Actor.objects.all().order_by('-num_of_films')[0:5],
        })
        return context

class ActorPage(TemplateView):
    template_name = 'front_end/actor_page.html'

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
        layout=go.Layout(title="Films by Gross", xaxis= {'title':'Year'}, yaxis={'title':'Gross'})
        figure=go.Figure(data=data,layout=layout)
        scatter_div = plot(figure, auto_open=False, output_type='div')

        context.update({
            'actor_detail': actor,
            #'total_gross': actor_data.average_box_office_return,
            'actor_film_list': actor_film_list,
            #'film_average': actor_data.average_return,
            #'weeks_in_cinema': actor_data.weeks_at_uk_cinemas,
            #'career_screen_average': actor_data.career_screen_average,
            'graph': scatter_div,
            #'bar_div':bar_div,
        })
        return context


class DirectorPage(TemplateView):
    template_name = 'front_end/director_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        director = Director.objects.get(imdb_id=kwargs['pk'])
        director_film_list = Film.objects.filter(director__imdb_id=str(director))
        director_model_data = director_film_list.filter(director__imdb_id=str(director)).values_list('release_date', 'gross','title', 'run_length', 'screen_average', 'opening')
        total_gross = sum(i[1] for i in director_model_data if i != None)
        weeks_in_cinema = sum(i[3] for i in director_model_data if i != None)
        career_screen_average = sum(i[4] for i in director_model_data if i != None)
        average_return = round(total_gross/len(director_film_list))

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
        layout=go.Layout(title="Films by Gross", xaxis= {'title':'Year'}, yaxis={'title':'Gross'})
        figure=go.Figure(data=data,layout=layout)
        scatter_div = plot(figure, auto_open=False, output_type='div')

        context.update({
            'director_detail': director,
            'total_gross': total_gross,
            'director_film_list': director_film_list,
            'film_average': average_return,
            'weeks_in_cinema': weeks_in_cinema,
            'career_screen_average':career_screen_average,
            'graph': scatter_div,
            #'bar_div':bar_div,
        })
        return context

class WriterPage(TemplateView):
    template_name = 'front_end/writer_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        writer = Writer.objects.get(imdb_id=kwargs['pk'])
        writer_film_list = Film.objects.filter(writers__imdb_id=str(writer))
        writer_model_data = writer_film_list.filter(writers__imdb_id=str(writer)).values_list('release_date', 'gross','title', 'run_length', 'screen_average', 'opening')
        total_gross = sum(i[1] for i in writer_model_data if i != None)
        weeks_in_cinema = sum(i[3] for i in writer_model_data if i != None)
        career_screen_average = sum(i[4] for i in writer_model_data if i != None)
        average_return = round(total_gross/len(writer_film_list))

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
        layout=go.Layout(title="Films by Gross", xaxis= {'title':'Year'}, yaxis={'title':'Gross'})
        figure=go.Figure(data=data,layout=layout)
        scatter_div = plot(figure, auto_open=False, output_type='div')

        context.update({
            'writer_detail': writer,
            'total_gross': total_gross,
            'writer_film_list': writer_film_list,
            'film_average': average_return,
            'weeks_in_cinema': weeks_in_cinema,
            'career_screen_average':career_screen_average,
            'graph': scatter_div,
            #'bar_div':bar_div,
        })
        return context

class SearchResults(ListView):
    template_name = 'front_end/search_page.html'
    context_object_name = 'query'
    paginate_by = 10
    
    def get_queryset(self):
        query_param = self.request.GET['q']
        film_search = Film.objects.filter(Q(title__icontains=query_param)).distinct()
        actor_search = Actor.objects.filter(Q(name__icontains=query_param)).distinct()
        director_search = Director.objects.filter(Q(name__icontains=query_param)).distinct()
        writer_search = Writer.objects.filter(Q(name__icontains=query_param)).distinct()

        return list(chain(film_search, actor_search, director_search, writer_search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'q_value': self.request.GET['q'],
        })

        # filter by a variable captured from url, for example
        return context