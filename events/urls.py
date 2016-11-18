from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^date/(?P<start_stamp>.+)/(?P<end_stamp>.+)$', views.show_date),
    url(r'^one_hundred_year', views.one_hundred_year),
    url(r'^viz$', views.viz_animation, name='viz'),
    url(r'^flooding$', views.basement_flooding, name='basement_flooding'),
    url(r'^$', views.viz_splash, name='splash'),
    url(r'^show-data$', views.index, name='show_data'),
    url(r'^about$', views.about, name='about')
]
