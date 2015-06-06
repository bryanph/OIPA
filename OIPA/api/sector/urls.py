from django.conf.urls import patterns, url
from api.sector import views
from django.views.decorators.cache import cache_page


urlpatterns = patterns(
    '',
    url(r'^$', 
        cache_page(60 * 60)(views.SectorList.as_view()), 
        name='sector-list'
    ),
    url(
        r'^/(?P<pk>[0-9]+)$',
        cache_page(60 * 60)(views.SectorDetail.as_view()),
        name='sector-detail'
    ),
    url(
        r'^/(?P<pk>[0-9]+)/activities$',
        cache_page(60 * 60)(views.SectorActivities.as_view()),
        name='sector-activities'
    ),
)
