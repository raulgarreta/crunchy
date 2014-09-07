from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#     (r'^$', direct_to_template, {'template': 'index.html',
#                                             'mimetype': 'html'}),

    url(r'^$', 'api.views.index', name='index'),

    # API
    url(r'^api/', include('api.urls', namespace="api")),

)



