# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        "Cleanup."
         # Can't use 'get' instead of 'filter' - there might be multiple records in the DB.
        orm['auth.permission'].objects.filter(codename='change_practitionerencounter').delete()
        orm['auth.permission'].objects.filter(codename='add_practitionerencounter').delete()
        orm['auth.permission'].objects.filter(codename='delete_practitionerencounter').delete()
        orm['contenttypes.contenttype'].objects.get(app_label='services', model='practitionerencounter').delete()

        # Note: PractitionerEncounter records have been deleted in the clients 0007 migration.
        # Note 2: There is no need to remove the PractitionerEncounter table, as it was a proxy model.


    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError("There is no way back.")

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
        'clients.district': {
            'Meta': {'object_name': 'District'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Region']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'clients.person': {
            'Meta': {'object_name': 'Person'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'clients.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
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
        },
        'services.asistservice': {
            'Meta': {'ordering': "('encounter',)", 'object_name': 'AsistService', '_ormbases': ['services.Service']},
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Service']", 'unique': 'True', 'primary_key': 'True'}),
            'where': ('fragapy.fields.models.MultiSelectField', [], {'max_length': '10'})
        },
        'services.diseasetest': {
            'Meta': {'ordering': "('encounter',)", 'object_name': 'DiseaseTest', '_ormbases': ['services.Service']},
            'disease': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'post_test_advice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pre_test_advice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Service']", 'unique': 'True', 'primary_key': 'True'}),
            'sign': ('django.db.models.fields.CharField', [], {'default': "'i'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'test_execution': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'services.encounter': {
            'Meta': {'ordering': "('-performed_on',)", 'object_name': 'Encounter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'performed_by': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'performed_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'encounters'", 'to': "orm['clients.Person']"}),
            'where': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Town']"})
        },
        'services.harmreduction': {
            'Meta': {'ordering': "('encounter',)", 'object_name': 'HarmReduction', '_ormbases': ['services.Service']},
            'acid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'alternatives': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'condoms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'in_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'medical_supplies': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'out_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'pregnancy_test': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Service']", 'unique': 'True', 'primary_key': 'True'}),
            'standard': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stericup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'svip_person_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'services.informationservice': {
            'Meta': {'ordering': "('encounter',)", 'object_name': 'InformationService', '_ormbases': ['services.Service']},
            'cure_possibilities': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'literature': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'medical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'safe_sex': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'safe_usage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Service']", 'unique': 'True', 'primary_key': 'True'}),
            'socio_legal': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'services.service': {
            'Meta': {'ordering': "('encounter',)", 'object_name': 'Service'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'encounter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': "orm['services.Encounter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'services.socialwork': {
            'Meta': {'ordering': "('encounter',)", 'object_name': 'SocialWork', '_ormbases': ['services.Service']},
            'counselling': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_mediation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Service']", 'unique': 'True', 'primary_key': 'True'}),
            'socio_legal': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'services.utilitywork': {
            'Meta': {'ordering': "('encounter',)", 'object_name': 'UtilityWork', '_ormbases': ['services.Service']},
            'refs': ('fragapy.fields.models.MultiSelectField', [], {'max_length': '40'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Service']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['services']
    symmetrical = True
