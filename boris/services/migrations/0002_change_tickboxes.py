# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'HarmReduction.jelly_capsules'
        db.delete_column('services_harmreduction', 'jelly_capsules')

        # Deleting field 'HarmReduction.cotton_filters'
        db.delete_column('services_harmreduction', 'cotton_filters')

        # Deleting field 'HarmReduction.sterilized_water'
        db.delete_column('services_harmreduction', 'sterilized_water')

        # Deleting field 'HarmReduction.alu_foil'
        db.delete_column('services_harmreduction', 'alu_foil')

        # Deleting field 'HarmReduction.alcohol_swabs'
        db.delete_column('services_harmreduction', 'alcohol_swabs')

        # Adding field 'HarmReduction.standard'
        db.add_column('services_harmreduction', 'standard', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'HarmReduction.alternatives'
        db.add_column('services_harmreduction', 'alternatives', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'SocialWork.socio_material'
        db.delete_column('services_socialwork', 'socio_material')

        # Adding field 'SocialWork.counselling'
        db.add_column('services_socialwork', 'counselling', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'HarmReduction.jelly_capsules'
        db.add_column('services_harmreduction', 'jelly_capsules', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'HarmReduction.cotton_filters'
        db.add_column('services_harmreduction', 'cotton_filters', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'HarmReduction.sterilized_water'
        db.add_column('services_harmreduction', 'sterilized_water', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'HarmReduction.alu_foil'
        db.add_column('services_harmreduction', 'alu_foil', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'HarmReduction.alcohol_swabs'
        db.add_column('services_harmreduction', 'alcohol_swabs', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'HarmReduction.standard'
        db.delete_column('services_harmreduction', 'standard')

        # Deleting field 'HarmReduction.alternatives'
        db.delete_column('services_harmreduction', 'alternatives')

        # Adding field 'SocialWork.socio_material'
        db.add_column('services_socialwork', 'socio_material', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'SocialWork.counselling'
        db.delete_column('services_socialwork', 'counselling')


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
            'where': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'services.crisisintervention': {
            'Meta': {'ordering': "('encounter',)", 'object_name': 'CrisisIntervention', '_ormbases': ['services.Service']},
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Service']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '1'})
        },
        'services.diseasetest': {
            'Meta': {'ordering': "('encounter',)", 'object_name': 'DiseaseTest', '_ormbases': ['services.Service']},
            'disease': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Service']", 'unique': 'True', 'primary_key': 'True'}),
            'sign': ('django.db.models.fields.CharField', [], {'default': "'i'", 'max_length': '1'})
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
            'svip': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['services']
