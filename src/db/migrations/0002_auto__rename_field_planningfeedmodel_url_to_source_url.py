# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('db_planningfeedmodel', 'url', 'source_url')


    def backwards(self, orm):
        db.rename_column('db_planningfeedmodel', 'source_url', 'url')


    models = {
        'db.planningfeedmodel': {
            'Meta': {'object_name': 'PlanningFeedModel'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['db']
