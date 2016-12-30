from django.conf.urls import url

from . import views

app_name = 'stats'

urlpatterns = [
        url(r'^$', views.index, name = 'index'),
        url(r'^team/$', views.teamView, name = 'team'),
        url(r'^challenge/$', views.challengeView, name = 'challenge'),
        url(r'^challenge/([0-9]+)/$', views.challengeDetailedView, name = 'detailedChallenge'),
        ]
