# -*- coding: utf-8 -*-

import json
import urllib
import urlparse

import oauth2
from linkedin import linkedin
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
    def get(self, request, format=None):
        lat = request.QUERY_PARAMS.get('lat', None)
        if lat is None:
            raise ParseError(detail="Must specify a valid lat argument.")
        lon = request.QUERY_PARAMS.get('lon', None)
        if lon is None:
            raise ParseError(detail="Must specify a valid lon argument.")
        # results = Event.objects.filter(finished=False).values_list("id", "name")

        result = []
        events = Event.objects.raw(
#         '''
#         SELECT id, name FROM
#           (SELECT id, name, lat, lon, (3959 * acos(cos(radians(%s)) * cos(radians(lat)) *
#                                              cos(radians(lon) - radians(%s)) +
#                                              sin(radians(%s)) * sin(radians(lat))))
#            AS distance
#            FROM api_event WHERE not finished) AS distances
#         WHERE distance < 1
#         ORDER BY distance
#         OFFSET 0
#         LIMIT 20;
#         ''',
#         [lat, lon, lat])

        '''
        SELECT id, name, lat, lon, picture_url, starts, css FROM api_event WHERE
        abs(lat - %s) < 0.018 and abs(lon - %s) < 0.018 and not finished;
        ''',
        [lat, lon])

        for event in events:
            result.append((event.id, event.name, event.lat, event.lon,
                           event.picture_url, event.starts, event.css))

        return Response(result)


class LogIn(APIView):
    '''
    Log in user.
    '''

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        user = User.objects.get(username=settings.DEBUG_USERNAME)
        token = Token.objects.get(user=user)
        result = {'api_token': token.key}
        current_events = {}
        for (id,) in user.profile.events.filter(finished=False).values_list("id"):
            current_events[id] = True
        result['current_events'] = current_events
        return Response(result)


