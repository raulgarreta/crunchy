import json

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


def random_member_id():
    import string, random
    return ''.join(random.choice(string.letters + string.digits) for i in xrange(50))
# # END random_member_id


class News(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(null=True)
    summary = models.TextField(max_length=500, null=True)
    picture_url = models.URLField(null=True)
    full_text = models.TextField(null=True)

    def __unicode__(self):
        return str(self.id) + ' - ' + self.name


class KeywordScore(models.Model):
    keyword = models.ForeignKey('Keyword')
    profile = models.ForeignKey('UserProfile')
    score = models.FloatField(default=0)

    def __unicode__(self):
        return self.profile.user.username + ' - ' + self.keyword.text + ' - ' + str(self.score)


class Keyword(models.Model):
    text = models.CharField(max_length=255, db_index=True)

    def __unicode__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    keywords = models.ManyToManyField(Keyword, related_name='users',
                                      through=KeywordScore)
    history = models.ManyToManyField(News, related_name='users')
    last_news = models.ManyToManyField(News, related_name='users')
    key_token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('member_id', 'user')
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created:
        rand_id = random_member_id()
        profile, new = UserProfile.objects.get_or_create(user=instance,
                                                         defaults={ 'member_id': rand_id })


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

