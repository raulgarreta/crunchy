'''
Created on Sep 06, 2014

@author: raul
'''

from rest_framework.serializers import ModelSerializer

from api.models import News


class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'date', 'tag', 'summary', 'image_url',
                  'content', 'url')


