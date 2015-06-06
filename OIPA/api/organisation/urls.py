from django.conf.urls import patterns, url
from api.organisation import views
from django.views.decorators.cache import cache_page


urlpatterns = patterns(
    '',
    url(
        r'^$', 
        cache_page(60 * 60)(views.OrganisationList.as_view()), 
        name='organisation-list'
    ),
    url(
        r'^/(?P<pk>[^@$&+,/:;=?]+)$',
        cache_page(60 * 60)(views.OrganisationDetail.as_view()),
        name='organisation-detail'
    ),
    url(
        r'^/(?P<pk>[^@$&+,/:;=?]+)/reported-activities$',
        cache_page(60 * 10)(views.ReportedActivities.as_view()),
        name='organisation-reported-activities'
    ),
    url(
        r'^/(?P<pk>[^@$&+,/:;=?]+)/participated-activities$',
        cache_page(60 * 10)(views.ParticipatedActivities.as_view()),
        name='organisation-participated-activities'
    ),
    url(
        r'^/(?P<pk>[^@$&+,/:;=?]+)/provided-transactions$',
        cache_page(60 * 10)(views.ProvidedTransactions.as_view()),
        name='organisation-provided-transactions'
    ),
    url(
        r'^/(?P<pk>[^@$&+,/:;=?]+)/received-transactions$',
        cache_page(60 * 10)(views.ReceivedTransactions.as_view()),
        name='organisation-received-transactions'
    ),

)
