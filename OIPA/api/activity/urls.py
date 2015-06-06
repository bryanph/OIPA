from django.conf.urls import patterns, url
import api.activity.views
import api.sector.views
from django.views.decorators.cache import cache_page


urlpatterns = patterns(
    '',
    url(r'^$',
        cache_page(60 * 60)(api.activity.views.ActivityList.as_view()),
        name='activity-list'),
    url(r'^/(?P<pk>[^@$&+,/:;=?]+)$',
        cache_page(60 * 60)(api.activity.views.ActivityDetail.as_view()),
        name='activity-detail'),
    url(r'^/(?P<pk>[^@$&+,/:;=?]+)/sectors$',
        cache_page(60 * 20)(api.activity.views.ActivitySectors.as_view()),
        name='activity-sectors'),
    url(r'^/(?P<pk>[^@$&+,/:;=?]+)/participating-orgs$',
        cache_page(60 * 10)(api.activity.views.ActivityParticipatingOrganisations.as_view()),
        name='activity-participating-organisations'),
    url(r'^/(?P<pk>[^@$&+,/:;=?]+)/recipient-countries$',
        cache_page(60 * 20)(api.activity.views.ActivityRecipientCountries.as_view()),
        name='activity-recipient-countries'),
    url(r'^/(?P<pk>[^@$&+,/:;=?]+)/recipient-regions',
        cache_page(60 * 20)(api.activity.views.ActivityRecipientRegions.as_view()),
        name='activity-recipient-regions'),
    url(r'^/(?P<pk>[^@$&+,/:;=?]+)/transactions',
        cache_page(60 * 10)(api.activity.views.ActivityTransactions.as_view(),
        name='activity-transactions'),
)
