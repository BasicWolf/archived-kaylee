from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^kaylee/', include('kaylee.frontends.django_frontend.urls'))
)
