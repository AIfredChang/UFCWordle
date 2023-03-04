from django.urls import path

from . import views
app_name = 'ufc_scraper'
urlpatterns = [
    # ex: /ufc_scraper/
    path('', views.index, name='index'),
    # ex: /ufc_scraper/5/
    path('<int:fighter_id>/', views.detail, name='detail'),
    # ex: /ufc_scraper/5/
    path('events/<int:fighter_id>/', views.fighter_events, name='events')

]