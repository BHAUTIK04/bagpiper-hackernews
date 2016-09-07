from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.news_view),
    url(r'^details/(?P<newsid>[0-9]+)', views.detail_view),
#     url(r'^', views.home_view),
#     url(r'^', views.home_view),
]