# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        orm['clients.DiseaseTest'].objects.filter(result=1).update(result=4)
        orm['clients.DiseaseTest'].objects.filter(result=2).update(result=1)
        orm['clients.DiseaseTest'].objects.filter(result=3).update(result=2)
        orm['clients.DiseaseTest'].objects.filter(result=4).update(result=3)
        orm['clients.DiseaseTest'].objects.filter(result=6).update(result=0)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'clients.anamnesis': {
            'Meta': {'object_name': 'Anamnesis'},
            'accomodation': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '8'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'been_cured_before': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'been_cured_currently': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'client': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clients.Client']", 'unique': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'drugs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clients.Drug']", 'through': "orm['clients.DrugUsage']", 'symmetrical': 'False'}),
            'education': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'employment': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'ethnic_origin': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'filled_when': ('django.db.models.fields.DateField', [], {}),
            'filled_where': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Town']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lives_with_junkies': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'living_condition': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '7'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'nationality': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'}),
            'risky_manners': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clients.RiskyBehavior']", 'through': "orm['clients.RiskyManners']", 'symmetrical': 'False'})
        },
        'clients.anonymous': {
            'Meta': {'unique_together': "(('sex', 'drug_user_type'),)", 'object_name': 'Anonymous', '_ormbases': ['clients.Person']},
            'drug_user_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clients.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'sex': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'clients.client': {
            'Meta': {'object_name': 'Client', '_ormbases': ['clients.Person']},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate_year_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'close_person': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '63'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['clients.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'primary_drug': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Drug']", 'null': 'True', 'blank': 'True'}),
            'primary_drug_usage': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sex_partner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Town']"})
        },
        'clients.clientnote': {
            'Meta': {'ordering': "('-datetime', '-id')", 'object_name': 'ClientNote'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notes_added'", 'to': "orm['auth.User']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notes'", 'to': "orm['clients.Client']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'clients.diseasetest': {
            'Meta': {'unique_together': "(('disease', 'anamnesis'),)", 'object_name': 'DiseaseTest'},
            'anamnesis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Anamnesis']"}),
            'disease': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '6'})
        },
        'clients.district': {
            'Meta': {'object_name': 'District'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Region']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'clients.drug': {
            'Meta': {'object_name': 'Drug'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'clients.drugusage': {
            'Meta': {'unique_together': "(('drug', 'anamnesis'),)", 'object_name': 'DrugUsage'},
            'anamnesis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Anamnesis']"}),
            'application': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'drug': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Drug']"}),
            'first_try_age': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'first_try_application': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'first_try_iv_age': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'was_first_illegal': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'clients.person': {
            'Meta': {'object_name': 'Person'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'clients.practitionercontact': {
            'Meta': {'object_name': 'PractitionerContact'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'person_or_institution': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['clients.Town']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'clients.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'clients.riskybehavior': {
            'Meta': {'object_name': 'RiskyBehavior'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'clients.riskymanners': {
            'Meta': {'unique_together': "(('behavior', 'anamnesis'),)", 'object_name': 'RiskyManners'},
            'anamnesis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Anamnesis']"}),
            'behavior': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.RiskyBehavior']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'periodicity_in_past': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'periodicity_in_present': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'clients.town': {
            'Meta': {'object_name': 'Town'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['clients']
    symmetrical = True
