from django.conf.urls import patterns, include, url
from kaylee.controller import app_name_pattern
from kaylee.node import node_id_pattern

urlpatterns = patterns('kaylee.contrib.frontends.django_frontend.views',
    url(r'^register$', 'register_node'),
    url(r'^apps/(?P<app_name>{})/subscribe/(?P<node_id>{})$'
        .format(app_name_pattern, node_id_pattern), 'subscribe_node'),
    url(r'^actions/(?P<node_id>{})$'.format(node_id_pattern), 'actions'),
)
