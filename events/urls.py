from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^date/(?P<start_stamp>.+)/(?P<end_stamp>.+)$', views.show_date),
    url(r'^$', views.index, name='index'),
]
