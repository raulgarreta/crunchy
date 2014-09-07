import re
import json
import datetime

import nltk
from django.utils import timezone

# from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from api.models import News


ALLOWED_CATEGORIES = ['Fundings & Exits', 'Startups', 'Mobile', 'Gadgets',
    'Enterprise', 'Social', 'Europe', 'Asia', 'CrunchGov', 'Apps',
    'Entertainment', 'Advertising Tech', 'Gaming', 'Media']


class Command(BaseCommand):
    def handle(self, *args, **options):
        f = open('../../../techcrunch_spider/items.json')
        news = json.loads(f.read())
        for i, new in enumerate(news):
            tags = json.loads(new['tags'])
            for tag in tags:
                if tag in ALLOWED_CATEGORIES:
                    m = re.search('\d\d\d\d/\d\d/\d\d', new['url'])
                    if m:
                        date_string = m.group(0)
                        dt = datetime.datetime.strptime(date_string, '%Y/%m/%d')
                    else:
                        continue
                    p = News.objects.create(url=new['url'][0:1024],
                                            title=new['title'],
                                            content=new['content'],
                                            tag=tag,
                                            image_url=new['url_image'][0:1024],
                                            date=dt)


def import_json():

    f = open(settings.ROOT_DIR + '/techcrunch_spider/items.json')
    news = json.loads(f.read())
    for i, new in enumerate(news):
        tags = json.loads(new['tags'])
        for tag in tags:
            if tag in ALLOWED_CATEGORIES:
                m = re.search('\d\d\d\d/\d\d/\d\d', new['url'])
                if m:
                    date_string = m.group(0)
                    dt = datetime.datetime.strptime(date_string, '%Y/%m/%d')
                else:
                    continue

                sents = nltk.sent_tokenize(new['content'])
                summary = ' '.join(sents[:5])

                p = News.objects.create(url=new['url'][0:1024],
                                        title=new['title'],
                                        content=new['content'],
                                        tag=tag,
                                        image_url=new['url_image'][0:1024],
                                        date=dt,
                                        summary=summary)

