from django.conf.urls import url

from . import views

app_name = 'challenges'

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'start/$', views.start, name='start'),
        url(r'([0-9]+)/$', views.challenge, name='challenge'),
        url(r'([0-9]+)/unlock/$', views.unlock, name='unlock'),
        url(r'([0-9]+)/hint/$', views.hint, name='hint'),
        url(r'([0-9]+)/(.+)/$', views.file, name='file'),
            ]
