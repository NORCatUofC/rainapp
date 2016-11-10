from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^reversals/', views.reversals),
    url(r'^$', views.index, name='index'),
]
