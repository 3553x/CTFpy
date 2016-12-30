from django.conf.urls import url

from . import views

app_name = 'user'

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.u_login, name='login'),
        url(r'^logout/$', views.u_logout, name='logout'),
        ]
