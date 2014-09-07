# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table(u'api_news', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('tag', self.gf('django.db.models.fields.TextField')()),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'api', ['News'])

        # Adding model 'KeywordScore'
        db.create_table(u'api_keywordscore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Keyword'])),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.UserProfile'])),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'api', ['KeywordScore'])

        # Adding model 'Keyword'
        db.create_table(u'api_keyword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'api', ['Keyword'])

        # Adding model 'UserProfile'
        db.create_table(u'api_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('key_token', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'api', ['UserProfile'])

        # Adding M2M table for field history on 'UserProfile'
        m2m_table_name = db.shorten_name(u'api_userprofile_history')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'api.userprofile'], null=False)),
            ('news', models.ForeignKey(orm[u'api.news'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'news_id'])

        # Adding M2M table for field last_news on 'UserProfile'
        m2m_table_name = db.shorten_name(u'api_userprofile_last_news')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'api.userprofile'], null=False)),
            ('news', models.ForeignKey(orm[u'api.news'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'news_id'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table(u'api_news')

        # Deleting model 'KeywordScore'
        db.delete_table(u'api_keywordscore')

        # Deleting model 'Keyword'
        db.delete_table(u'api_keyword')

        # Deleting model 'UserProfile'
        db.delete_table(u'api_userprofile')

        # Removing M2M table for field history on 'UserProfile'
        db.delete_table(db.shorten_name(u'api_userprofile_history'))

        # Removing M2M table for field last_news on 'UserProfile'
        db.delete_table(db.shorten_name(u'api_userprofile_last_news'))


    models = {
        u'api.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'api.keywordscore': {
            'Meta': {'object_name': 'KeywordScore'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Keyword']"}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.UserProfile']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'api.news': {
            'Meta': {'object_name': 'News'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'summary': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'api.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'history': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_history'", 'symmetrical': 'False', 'to': u"orm['api.News']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'through': u"orm['api.KeywordScore']", 'to': u"orm['api.Keyword']"}),
            'last_news': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_last_news'", 'symmetrical': 'False', 'to': u"orm['api.News']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['api']