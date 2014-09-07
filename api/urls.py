# -*- coding: utf-8 -*-
from __future__ import (
    print_function, unicode_literals, division, absolute_import)

from django.conf.urls.defaults import url, patterns, include
from django.conf import settings
from rest_framework import routers

from api.views import (NewsHistory, LastNewsList,
                       GetAPIToken,
                       LogIn)
                       # IsAuthenticated, LogOut)


router = routers.SimpleRouter()

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),

    url(r'^get_api_token/$',
        GetAPIToken.as_view(), name='get_api_token'),

    url(r'^news_history/$',
        NewsHistory.as_view(), name='news_history'),

    url(r'^last_news_list/$',
        LastNewsList.as_view(), name='last_news_list'),

    url(r'^login/$',
        LogIn.as_view(), name='login'),

)

# if settings.DEBUG:
#     urlpatterns += patterns(
#         '',
#
#         url(r'^login/$',
#             LogIn.as_view(), name='login'),
#
#     )


