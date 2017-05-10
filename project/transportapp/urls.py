from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/', views.add, name='add'),
    url(r'^add_detail/(?P<pk>[0-9]+)/', views.add_detail, name='add_detail'),
    url(r'^add_stand/', views.add_stand, name='add_stand'),
    url(r'^add_detail_stand/(?P<pk>[0-9]+)/', views.add_detail_stand, name='add_detail_stand'),
#    url(r'^show/', views.show, name='show'),
    url(r'^show_res/(?P<pk>[0-9]+)/', views.show_res, name='show_res'),
#    url(r'^about/', views.about, name='about'),
    ]
