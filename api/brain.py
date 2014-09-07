'''
Created on Sep 6, 2014

@author: raul
'''


# from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

import operator

# from models import Post, TwitterUser
from utils import *
import json

from api.models import UserProfile
from django.contrib.auth.models import User


def profile(twitter_account):

    user, created = User.objects.get_or_create(username=twitter_account)

    if created:
        api = registerAPI()
        descriptions = get_friends_description(api, twitter_account)  # request.GET['twitter_account'])
        lang_classifications = classify_batch_lang(descriptions)
        descriptions = [description for description, lang
            in zip(descriptions, lang_classifications) if lang[0][0] == 'English']
        # expanded_descriptions = []
        # for description in descriptions:
        #     expanded = expand_query(description)
        #     if expanded:
        #         expanded_descriptions.append(expanded)
        #     elif description:
        #         expanded_descriptions.append(description)
        # expanded_descriptions = [expand_query(description) for description in descriptions]
        classifications = classify_batch_text(descriptions)

        # raise Exception(str(classifications) + str(descriptions))

        categories = {}
        for classification in classifications:
            if float(classification[0][1]) < 0.4 or float(classification[-1][1]) < 0.4:
                continue

            category = str(classification[0][0])  # + '|' + classification[-1][0]
            if not category in categories:
                categories[category] = 0
            categories[category] += 1

        # sort categories by value in reversed order
        sorted_categories = sorted(categories.iteritems(), key=operator.itemgetter(1))[::-1]
        user.profile.sorted_categories = json.dumps(sorted_categories)
        user.profile.save()

    else:
        sorted_categories = user.profile.sorted_categories

    print sorted_categories
    return sorted_categories

#             total_classifications = sum([category[1] for category in sorted_categories])
#             max_articles = 50
#
#             articles = []
#             data_plot = []
#             for category in sorted_categories:
#                 number_of_articles = int(max_articles * (float(category[1]) / total_classifications))
#                 father_category, child_category = category[0].split('|')
#                 articles.extend(list(Post.objects.filter(Q(category_father=father_category),
#                                 Q(category_child1=child_category) |
#                                 Q(category_child2=child_category) |
#                                 Q(category_child3=child_category))
#                         .exclude(pk__in=[article.id for article in articles])
#                         .order_by('-date_time')[0:number_of_articles]))
#                 data_plot.append({"label": category[0].replace('|', ' -> ').title().replace('Us', 'US'),
#                                  "data": number_of_articles})
#
#             for article in articles:
#                 if article.image_url.startswith('/media'):
#                     article.image_url = 'http://rack.3.mshcdn.com' + article.image_url
#                 elif article.image_url.startswith('media/'):
#                     article.image_url = 'http://rack.3.mshcdn.com/' + article.image_url

#             # try:
#             api = registerAPI()
#             t_user = api.get_user(twitter_user.twitter_account)
#             # except:
#             #     print "error"
#             #     t_user = {}



