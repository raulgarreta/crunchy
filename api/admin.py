'''
Created on Sep 06, 2014

@author: raul
'''


from api.models import UserProfile, Keyword, KeywordScore, News
from django.contrib import admin


class UserProfileAdmin(admin.ModelAdmin):
    pass


class NewsAdmin(admin.ModelAdmin):
    list_filter = ['tag']


admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(News, NewsAdmin)

