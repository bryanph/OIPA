from django.conf.urls import patterns, url
from api.country import views
from django.views.decorators.cache import cache_page

urlpatterns = patterns(
    '',
    url(
        r'^$', 
        cache_page(60 * 60)(views.CountryList.as_view()), 
        name='country-list'
    ),
    url(
        r'^/(?P<pk>[A-Za-z]+)$',
        cache_page(60 * 60)(views.CountryDetail.as_view()),
        name='country-detail'
    ),
    url(
        r'^/(?P<pk>[A-Za-z]+)/activities$',
        cache_page(60 * 10)(views.CountryActivities.as_view()),
        name='country-activities'
    ),
    url(
        r'^/(?P<pk>[A-Za-z]+)/indicators$',
        cache_page(60 * 10)(views.CountryIndicators.as_view()),
        name='country-indicators'
    ),
    url(
        r'^/(?P<pk>[A-Za-z]+)/cities$',
        cache_page(60 * 10)(views.CountryCities.as_view()),
        name='country-cities'
    ),
)
