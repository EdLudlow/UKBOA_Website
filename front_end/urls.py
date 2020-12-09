from django.urls import path, include
from front_end import views

app_name = 'front_end'

urlpatterns = [

    #Home page and About
    path('', views.HomePage.as_view(), name='home'),
    path('the_site', views.AboutTheSite.as_view(), name='about'),
    path('contact', views.AboutMe.as_view(), name='creator'),

    #Entries
    path('film_page/<pk>/', views.FilmPage.as_view()),
    path('actor_page/<pk>/',views.ActorPage.as_view(), name='actor_page'),
    path('director_page/<pk>/',views.DirectorPage.as_view(), name='director_page'),
    path('writer_page/<pk>', views.WriterPage.as_view(), name='writer_page'),

    #Film Overviews
    path('general_films_page', views.GeneralFilmsPage.as_view(), name='general_films_page'),

    #Actor overviews
    path('actor_overview', views.ActorOverview.as_view(), name='actor_overview'),
    path('top_actors_by_bo', views.ActorOverviewTopAtBO.as_view(), name='actor_top_at_bo'),
    path('top_actors_by_length', views.ActorOverviewLengthAtBO.as_view(), name='actor_top_by_length'),
    path('top_actors_by_films', views.ActorOverviewNumFilms.as_view(), name='actor_top_by_films'),

    #director overviews
    path('director_overview', views.DirectorOverview.as_view(), name='director_overview'),
    path('top_directors_by_bo', views.DirectorOverviewTopAtBO.as_view(), name='director_top_at_bo'),
    path('top_directors_by_length', views.DirectorOverviewLengthAtBO.as_view(), name='director_top_by_length'),
    path('top_directors_by_films', views.DirectorOverviewNumFilms.as_view(), name='director_top_by_films'),

    #Writer overviews
    path('writer_overview', views.WriterOverview.as_view(), name='writer_overview'),
    path('top_writers_by_bo', views.WriterOverviewTopAtBO.as_view(), name='writer_top_at_bo'),
    path('top_writers_by_length', views.WriterOverviewLengthAtBO.as_view(), name='writer_top_by_length'),
    path('top_writers_by_films', views.WriterOverviewNumFilms.as_view(), name='writer_top_by_films'),

    #search page
    path('results/', views.SearchResults.as_view(), name='search_page'),
]