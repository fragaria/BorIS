# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Drug'
        db.create_table('clients_drug', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
        ))
        db.send_create_signal('clients', ['Drug'])

        # Adding model 'Region'
        db.create_table('clients_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
        ))
        db.send_create_signal('clients', ['Region'])

        # Adding model 'District'
        db.create_table('clients_district', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Region'])),
        ))
        db.send_create_signal('clients', ['District'])

        # Adding model 'Town'
        db.create_table('clients_town', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.District'])),
        ))
        db.send_create_signal('clients', ['Town'])

        # Adding model 'Person'
        db.create_table('clients_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('clients', ['Person'])

        # Adding model 'PractitionerContact'
        db.create_table('clients_practitionercontact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person_or_institution', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('town', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['clients.Town'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('clients', ['PractitionerContact'])

        # Adding M2M table for field users on 'PractitionerContact'
        m2m_table_name = db.shorten_name('clients_practitionercontact_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('practitionercontact', models.ForeignKey(orm['clients.practitionercontact'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['practitionercontact_id', 'user_id'])

        # Adding model 'Anonymous'
        db.create_table('clients_anonymous', (
            ('person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['clients.Person'], unique=True, primary_key=True)),
            ('drug_user_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('sex', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('clients', ['Anonymous'])

        # Adding unique constraint on 'Anonymous', fields ['sex', 'drug_user_type']
        db.create_unique('clients_anonymous', ['sex', 'drug_user_type'])

        # Adding model 'Client'
        db.create_table('clients_client', (
            ('person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['clients.Person'], unique=True, primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=63)),
            ('sex', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=63, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=63, null=True, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('birthdate_year_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('town', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Town'])),
            ('primary_drug', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Drug'], null=True, blank=True)),
            ('primary_drug_usage', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('close_person', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sex_partner', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('clients', ['Client'])

        # Adding model 'Anamnesis'
        db.create_table('clients_anamnesis', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('client', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['clients.Client'], unique=True)),
            ('filled_when', self.gf('django.db.models.fields.DateField')()),
            ('filled_where', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Town'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('nationality', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=4)),
            ('ethnic_origin', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3)),
            ('living_condition', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=7)),
            ('accomodation', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=8)),
            ('lives_with_junkies', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('employment', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('education', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('been_cured_before', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('been_cured_currently', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('clients', ['Anamnesis'])

        # Adding model 'ClientNote'
        db.create_table('clients_clientnote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notes_added', to=orm['auth.User'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notes', to=orm['clients.Client'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('clients', ['ClientNote'])

        # Adding model 'DrugUsage'
        db.create_table('clients_drugusage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('drug', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Drug'])),
            ('anamnesis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Anamnesis'])),
            ('application', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('frequency', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('first_try_age', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('first_try_iv_age', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('first_try_application', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('was_first_illegal', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('clients', ['DrugUsage'])

        # Adding unique constraint on 'DrugUsage', fields ['drug', 'anamnesis']
        db.create_unique('clients_drugusage', ['drug_id', 'anamnesis_id'])

        # Adding model 'RiskyManners'
        db.create_table('clients_riskymanners', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('behavior', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('anamnesis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Anamnesis'])),
            ('periodicity_in_past', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('periodicity_in_present', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('clients', ['RiskyManners'])

        # Adding unique constraint on 'RiskyManners', fields ['behavior', 'anamnesis']
        db.create_unique('clients_riskymanners', ['behavior', 'anamnesis_id'])

        # Adding model 'DiseaseTest'
        db.create_table('clients_diseasetest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('anamnesis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Anamnesis'])),
            ('disease', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('result', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('clients', ['DiseaseTest'])

        # Adding unique constraint on 'DiseaseTest', fields ['disease', 'anamnesis']
        db.create_unique('clients_diseasetest', ['disease', 'anamnesis_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'DiseaseTest', fields ['disease', 'anamnesis']
        db.delete_unique('clients_diseasetest', ['disease', 'anamnesis_id'])

        # Removing unique constraint on 'RiskyManners', fields ['behavior', 'anamnesis']
        db.delete_unique('clients_riskymanners', ['behavior', 'anamnesis_id'])

        # Removing unique constraint on 'DrugUsage', fields ['drug', 'anamnesis']
        db.delete_unique('clients_drugusage', ['drug_id', 'anamnesis_id'])

        # Removing unique constraint on 'Anonymous', fields ['sex', 'drug_user_type']
        db.delete_unique('clients_anonymous', ['sex', 'drug_user_type'])

        # Deleting model 'Drug'
        db.delete_table('clients_drug')

        # Deleting model 'Region'
        db.delete_table('clients_region')

        # Deleting model 'District'
        db.delete_table('clients_district')

        # Deleting model 'Town'
        db.delete_table('clients_town')

        # Deleting model 'Person'
        db.delete_table('clients_person')

        # Deleting model 'PractitionerContact'
        db.delete_table('clients_practitionercontact')

        # Removing M2M table for field users on 'PractitionerContact'
        db.delete_table(db.shorten_name('clients_practitionercontact_users'))

        # Deleting model 'Anonymous'
        db.delete_table('clients_anonymous')

        # Deleting model 'Client'
        db.delete_table('clients_client')

        # Deleting model 'Anamnesis'
        db.delete_table('clients_anamnesis')

        # Deleting model 'ClientNote'
        db.delete_table('clients_clientnote')

        # Deleting model 'DrugUsage'
        db.delete_table('clients_drugusage')

        # Deleting model 'RiskyManners'
        db.delete_table('clients_riskymanners')

        # Deleting model 'DiseaseTest'
        db.delete_table('clients_diseasetest')


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
            'nationality': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'})
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
            'result': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
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
        'clients.riskymanners': {
            'Meta': {'unique_together': "(('behavior', 'anamnesis'),)", 'object_name': 'RiskyManners'},
            'anamnesis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clients.Anamnesis']"}),
            'behavior': ('django.db.models.fields.PositiveIntegerField', [], {}),
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