from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'kl_django.views.index'),
    url(r'^kaylee/', include('kaylee.contrib.frontends.django_frontend.urls'))
)
