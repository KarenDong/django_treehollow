from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^hollow$', views.hollow),
    url(r'^users/(?P<id>\d+)$', views.viewUser),
    url(r'add$',views.add),
    url(r'^hollow/(?P<id>\d+)$', views.viewHollow),
    url(r'^remove/(?P<id>\d+)$',views.remove),
    url(r'^logout$',views.logout)
]
