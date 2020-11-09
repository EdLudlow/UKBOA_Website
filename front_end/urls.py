from django.urls import path, include
from front_end import views

app_name = 'front_end'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('film_page/<pk>/', views.FilmPage.as_view()),
    path('general_films_page', views.GeneralFilmsPage.as_view(), name='general_films_page'),

    #Actor overviews
    path('actor_overview', views.ActorOverview.as_view(), name='actor_overview'),
    path('top_actors_by_bo', views.ActorOverviewTopAtBO.as_view(), name='actor_top_at_bo'),
    path('top_actors_by_length', views.ActorOverviewLengthAtBO.as_view(), name='actor_top_by_length'),
    path('top_actors_by_films', views.ActorOverviewNoFilms.as_view(), name='actor_top_by_films'),


    path('actor_page/<pk>/',views.ActorPage.as_view(), name='actor_page'),
    path('director_page/<pk>/',views.DirectorPage.as_view(), name='director_page'),
    path('writer_page/<pk>', views.WriterPage.as_view(), name='writer_page'),
    #path('results/', views.search, name='search_page'),
    path('results/', views.SearchResults.as_view(), name='search_page')
]