# -*- coding: utf-8 -*-

import json
import urllib
import urlparse
from datetime import date, timedelta, datetime

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.authtoken.models import Token

from api.models import UserProfile, News
from api.models import Keyword, KeywordScore
from api.serializers import NewsSerializer
from api.brain import profile


profile_field_map = {
    'member_id'             : 'id',
    'first_name'            : 'firstName',
    'last_name'             : 'lastName',
    'headline'              : 'headline',
    'location'              : 'location',
    'industry'              : 'industry',
#     'num_connections'       : 'num_connections',
#     'num_connections_capped': 'num_connections_capped',
    'summary'               : 'summary',
#     'main_address'          : 'main_address',
    'picture_url'           : 'pictureUrl',
    'skills'                : 'skills',
    'interests'             : 'interests',
}


def index(request):
    context = {}
    return render_to_response('index.html', context,
                              context_instance=RequestContext(request))


class GetAPIToken(APIView):
    '''
    Endpoint to get the API key from the key generated at authorization step.
    '''

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # get query parameters
        token = request.QUERY_PARAMS.get('token', None)
        if token is None:
            raise ParseError(detail="Must specify a valid token argument.")

        profile = UserProfile.objects.get(key_token=token)
        token = Token.objects.get(user=profile.user)
        result = {'api_token': token.key}
        current_events = {}
        for (id,) in profile.events.filter(finished=False).values_list("id"):
            current_events[id] = True
        result['current_events'] = current_events
        return Response(result)


class NewsHistory(APIView):
    '''
    Get the event history listing of the current user.
    Returns a list of tuples (id, name, description, type)
    '''
    def get(self, request, format=None):
        result = request.user.profile.events.filter(finished=True).values_list("id", "name", "picture_url", "starts", "css")
        return Response(result)


class LastNewsList(APIView):
    '''
    Given a geolocation, return a list of events near that location.
    Returns a list of tuples (id, name, description, type)
    '''
    def post(self, request, format=None):

        twitter_account = request.QUERY_PARAMS.get('twitter_account', None)
        if twitter_account is None:
            raise ParseError(detail="Must specify a valid twitter_account argument.")

        try:
            user = User.objects.get(username=twitter_account)
        except:
            raise ParseError(detail="The specified user does not exist.")

#         news_list = News.objects.filter(date__gte=datetime.now() - timedelta(days=3))
        return recommend(user)


def recommend(user):

    result = []
    sorted_categories = json.loads(user.profile.sorted_categories)
    print sorted_categories

    total_classifications = 0
    for category, n in sorted_categories:
        total_classifications += n

    max_articles = 10
    delta_days = 3

    articles = []
    for category in sorted_categories:
        print category
        number_of_articles = int(max_articles * (float(category[1]) / total_classifications))
        father_category = category[0]
        articles.extend(list(News.objects.filter(date__gte=datetime.now() - timedelta(days=delta_days))
                .filter(tag=father_category)
                .exclude(pk__in=[article.id for article in articles])
                .order_by('-date')[0:number_of_articles]))

    for n in articles:
        result.append(NewsSerializer(n).data)

    return Response(result)


class LogIn(APIView):
    '''
    Log in user.
    '''

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        twitter_account = request.QUERY_PARAMS.get('twitter_account', None)
        if twitter_account is None:
            raise ParseError(detail="Must specify a valid twitter_account argument.")

        # user_profile = UserProfile.objects.get(twitter_account=twitter_account)

        categories = profile(twitter_account)

        return Response(categories)


