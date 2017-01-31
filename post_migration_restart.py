"""
This is script should bring existing installations in line with the state
in repository. It is supposed to be run after:

  1. The migration_restart branch has been merged to master and deployed.
  2. south_migrationhistory has been truncated.
  3. The initial migrations for clients and services have been faked.

"""

from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.db.models import get_models, get_app

from boris.services.management import proxy_permissions_fix

# First, create the missing permissions.
create_permissions(get_app('services'), get_models(), 2)

# Then remove the obsolete permissions.

# Obsolete models
contenttypes = (
    ('services', 'crisisintervention'),
    ('clients', 'riskybehavior'),
)
for app_label, model in contenttypes:
    try:
        ct = ContentType.objects.get(app_label=app_label, model=model)
    except ContentType.DoesNotExist:
        print 'ContentType for %s not found!' % model
    else:
        qset = Permission.objects.filter(content_type=ct)
        print "Deleting %i permissions for %s" % (qset.count(), model)
        qset.delete()

# Remove services proxy permissions.
services_ct = ContentType.objects.get(app_label='services', model='service')
codenames = [
    'add_utilitywork',
    'change_utilitywork',
    'delete_utilitywork',
    'add_incomeexamination',
    'change_incomeexamination',
    'delete_incomeexamination',
    'add_individualcounselling',
    'change_individualcounselling',
    'delete_individualcounselling',
    'add_phoneusage',
    'change_phoneusage',
    'delete_phoneusage',
]
print "Deleting the proxy permissions: %s" % ', '.join(codenames)
for codename in codenames:
    qset = Permission.objects.filter(codename=codename, content_type=services_ct)
    if qset.count() != 1:
        print "Something's wrong with the %s permission." % codename
    else:
        qset.delete()

# Run the proxy permissions fix hook.
services = get_app('services')
proxy_permissions_fix.delete_proxy_permissions(services, get_models(services), 2)

# Delete the obsolete contenttypes.
contenttypes = (
    ('clients', 'riskybehavior'),
    ('services', 'practitionerencounter'),
)
for app_label, model in contenttypes:
    try:
        ct = ContentType.objects.get(app_label=app_label, model=model)
    except ContentType.DoesNotExist:
        print 'ContentType for %s not found!' % model
    else:
        print "Deleting contenttype: %s, %s" % (app_label, model)
        ct.delete()

# Finally, reload the group permissions fixture.
call_command('loaddata', 'groups.json')
