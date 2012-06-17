# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Encounter'
        db.create_table('services_encounter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='encounters', to=orm['clients.Person'])),
            ('performed_on', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('where', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Town'])),
        ))
        db.send_create_signal('services', ['Encounter'])

        # Adding M2M table for field performed_by on 'Encounter'
        db.create_table('services_encounter_performed_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('encounter', models.ForeignKey(orm['services.encounter'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('services_encounter_performed_by', ['encounter_id', 'user_id'])

        # Adding model 'Service'
        db.create_table('services_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('encounter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='services', to=orm['services.Encounter'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('services', ['Service'])

        # Adding model 'HarmReduction'
        db.create_table('services_harmreduction', (
            ('service_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.Service'], unique=True, primary_key=True)),
            ('in_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('out_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('svip', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('sterilized_water', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cotton_filters', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('alcohol_swabs', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('acid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('alu_foil', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('condoms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('jelly_capsules', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('stericup', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('other', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pregnancy_test', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('medical_supplies', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('services', ['HarmReduction'])

        # Adding model 'DiseaseTest'
        db.create_table('services_diseasetest', (
            ('service_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.Service'], unique=True, primary_key=True)),
            ('disease', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('sign', self.gf('django.db.models.fields.CharField')(default='i', max_length=1)),
        ))
        db.send_create_signal('services', ['DiseaseTest'])

        # Adding model 'AsistService'
        db.create_table('services_asistservice', (
            ('service_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.Service'], unique=True, primary_key=True)),
            ('where', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('services', ['AsistService'])

        # Adding model 'InformationService'
        db.create_table('services_informationservice', (
            ('service_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.Service'], unique=True, primary_key=True)),
            ('safe_usage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('safe_sex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('medical', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('socio_legal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cure_possibilities', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('literature', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('other', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('services', ['InformationService'])

        # Adding model 'CrisisIntervention'
        db.create_table('services_crisisintervention', (
            ('service_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.Service'], unique=True, primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='d', max_length=1)),
        ))
        db.send_create_signal('services', ['CrisisIntervention'])

        # Adding model 'SocialWork'
        db.create_table('services_socialwork', (
            ('service_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.Service'], unique=True, primary_key=True)),
            ('socio_legal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('socio_material', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('service_mediation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('other', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('services', ['SocialWork'])


    def backwards(self, orm):
        
        # Deleting model 'Encounter'
        db.delete_table('services_encounter')

        # Removing M2M table for field performed_by on 'Encounter'
        db.delete_table('services_encounter_performed_by')

        # Deleting model 'Service'
        db.delete_table('services_service')

        # Deleting model 'HarmReduction'
        db.delete_table('services_harmreduction')

        # Deleting model 'DiseaseTest'
        db.delete_table('services_diseasetest')

        # Deleting model 'AsistService'
        db.delete_table('services_asistservice')

        # Deleting model 'InformationService'
        db.delete_table('services_informationservice')

        # Deleting model 'CrisisIntervention'
        db.delete_table('services_crisisintervention')

        # Deleting model 'SocialWork'
        db.delete_table('services_socialwork')


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
            'alcohol_swabs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'alu_foil': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'condoms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cotton_filters': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'in_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'jelly_capsules': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'medical_supplies': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'out_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'pregnancy_test': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Service']", 'unique': 'True', 'primary_key': 'True'}),
            'stericup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sterilized_water': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_mediation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['services.Service']", 'unique': 'True', 'primary_key': 'True'}),
            'socio_legal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'socio_material': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['services']
