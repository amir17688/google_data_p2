from django.conf.urls import patterns, url


urlpatterns = patterns('tidings.views',
    url(r'^unsubscribe/(?P<watch_id>\d+)$',
        'unsubscribe',
        name='tidings.unsubscribe')
)
