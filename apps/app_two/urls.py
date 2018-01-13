# APP 2
from django.conf.urls import url, include
from . import views

# This is app_two
urlpatterns = [
# root route to index method
    url(r'^$', views.index, name="index"),
    url(r'^add_plan$', views.add_plan, name="add_plan"),
    url(r'^destination/(?P<trip_id>\d+)$', views.destination, name="destination"),
    url(r'^join_trip/(?P<trip_id>\d+)$', views.join_trip, name="join_trip"),
    url(r'^logout$', views.logout, name="logout"),
]
