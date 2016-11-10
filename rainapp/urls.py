from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('events.urls')),
    url(r'^csos/', include('csos.urls')),
]