from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^date/(?P<start_stamp>.+)/(?P<end_stamp>.+)$', views.show_date),
    url(r'^nyear/(?P<recurrence>.+)', views.nyear),
    url(r'^viz$', views.viz_animation, name='viz'),
    url(r'^flooding$', views.basement_flooding, name='basement_flooding'),
    url(r'^$', views.index, name='index'),
]
