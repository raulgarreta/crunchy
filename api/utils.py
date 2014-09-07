from django.conf import settings

import tweepy
import json
import requests
from requests_oauthlib import OAuth1
from requests.adapters import HTTPAdapter
import re
import justext
from random import shuffle
import urllib


def classify_batch_text(text_list):
    """ Uses monkeylearn api to classify the given list texts."""

    data = {
        'func': 'absolute',
        'threshold': '0',
        'text_list': text_list
    }

    response = requests.post(settings.MONKEYLEARN_CLASSIFY_BATCH_TEXT_URL,
                      data=json.dumps(data),
                      headers={'Authorization': 'Token ' + settings.MONKEYLEARN_AUTHTOKEN,
                      'Content-Type': 'application/json'})
    try:
        return json.loads(response.text)
    except:
        raise Exception(response.text)


def classify_batch_lang(text_list):

    data = {
        'func': 'absolute',
        'threshold': '0',
        'text_list': text_list
    }

    response = requests.post(settings.MONKEYLEARN_LANG_CLASSIFY_BATCH_TEXT_URL,
                      data=json.dumps(data),
                      headers={'Authorization': 'Token ' + settings.MONKEYLEARN_LANG_AUTHTOKEN,
                      'Content-Type': 'application/json'})
    return json.loads(response.text)


def def_auth():
    """ Returns the authentication to use within the twitter api"""
    auth = tweepy.OAuthHandler(
        settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(
        settings.TWITTER_ACCESS_TOKEN_KEY, settings.TWITTER_ACCESS_TOKEN_SECRET)
    return auth


def registerAPI():
    """ Registers and returns the twitter api using tweepy python library """
    auth = def_auth()
    api = tweepy.API(auth)
    return api


def get_hashtags_tweets(tweet, api):
    """ Categorizes all the hashtags in the given tweet and returns a list of them """
    hashtags = re.findall(r'(#\S+)', tweet)
    tweets_of_hashtags = []
    for hashtag in hashtags:
        results = api.search(q=hashtag, lang='en', count=30)
        if results:
            tweets_hashtag = " ".join(
                [tweet_hashtag.text for tweet_hashtag in results])
            tweets_of_hashtags.append(tweets_hashtag)
    return tweets_of_hashtags


def get_url_text(tweet):
    urls = re.findall(r'(https?://\S+)', tweet)
    good_text = ''
    if urls:
        try:
            # response = requests.get(urls[0])
            s = requests.Session()
            s.mount(urls[0], HTTPAdapter(max_retries=1))
            response = s.get(urls[0])
            paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
            for paragraph in paragraphs:
                if not paragraph.is_boilerplate:
                    good_text += ' ' + paragraph.text
        except:
            pass
    return good_text


def get_friends_description(api, twitter_account):
    user_ids = api.friends_ids(twitter_account)
    shuffle(user_ids)
    user_ids = user_ids[0:100]
    auth = authenticate()
    response = requests.get(settings.TWITTER_GET_USERS_URL +
                            ','.join([str(user_id) for user_id in user_ids]),
                            auth=auth)
    users = json.loads(response.content)
    descriptions = []
    for user in users:
        if user['description']:
            description = re.sub(r'(https?://\S+)', '', user['description'])
            if len(re.split(r'[^0-9A-Za-z]+', description)) > 5:
                descriptions.append(description.strip('#').strip('@'))

    # for user_id in user_ids:
    #     twitter_user = api.get_user(user_id)
    #     if twitter_user.description:
    #         descriptions.append(twitter_user.description)
    return descriptions


def authenticate():
    return OAuth1(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET,
                  settings.TWITTER_ACCESS_TOKEN_KEY, settings.TWITTER_ACCESS_TOKEN_SECRET)


def expand_query(text):
    expanded_query = []
    param = {'q': unicode(text).encode('utf-8')}
    search = urllib.urlencode(param)
    response = requests.get(settings.SOLR_BROWSE_URL + search)
    json_resp = json.loads(response.text)
    for id, item in json_resp['highlighting'].iteritems():
        expanded_query.append((" ".join(item['content'])).replace('<b>', '').replace('</b>', ''))
    return " ".join(expanded_query)
