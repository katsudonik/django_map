
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.soil_disposal_tasks_list),
    url(r'^shot$', views.screen_shot_soil_locations_map),
]
