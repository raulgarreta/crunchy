'''
Created on Nov 24, 2013

@author: raul
'''


from api.models import UserProfile, Keyword, KeywordScore
from django.contrib import admin


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)

