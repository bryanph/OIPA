from django.conf.urls import patterns, url
from api.region import views
from django.views.decorators.cache import cache_page

urlpatterns = patterns(
    '',
    url(
        r'^$', 
        cache_page(60 * 60)(views.RegionList.as_view()), 
        name='region-list'
    ),
    url(
        r'^/(?P<pk>[0-9]+)$',
        cache_page(60 * 60)(views.RegionDetail.as_view()),
        name='region-detail'
    ),
    url(
        r'^/(?P<pk>[0-9]+)/countries$',
        cache_page(60 * 10)(views.RegionCountries.as_view()),
        name='region-countries'
    ),
    url(
        r'^/(?P<pk>[0-9]+)/activities$',
        cache_page(60 * 10)(views.RegionActivities.as_view()),
        name='region-activities'
    ),
)
