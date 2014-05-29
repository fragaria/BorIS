from copy import copy

from django.contrib.auth.models import User
from django.utils.functional import curry
from django.contrib.contenttypes.models import ContentType

from boris.clients.models import Client, Town, Region, District
from boris.classification import SEXES
from boris.services.models import Encounter


def get_testing_string_enum(ModelClass, title, *args, **kwargs):
    return ModelClass.objects.create(title=title, **kwargs)

get_testing_region = curry(get_testing_string_enum, Region, 'Stredocesky')
get_testing_district = curry(get_testing_string_enum, District, 'Rakovnik', region=get_testing_region())
get_tst_town = curry(get_testing_string_enum, Town, 'Rakovnik', district=get_testing_district())

def get_tst_client(code='borivoj22', cdata=None):
    client_data = {
         'code': code,
         'sex': SEXES.MALE,
         'birthdate': '1980-10-10',
         'town': get_tst_town(),
         'content_type': ContentType.objects.get_for_model(Client)
    }

    if cdata:
        client_data.update(cdata)

    return Client.objects.create(**client_data)


def get_tst_usr(username='strachkvas'):
    user_data = {
        'username': username,
        'is_staff': True,
        'is_active': True,
        'is_superuser': True,
    }

    user = User.objects.create(**user_data)

    password = 'heslo'
    user.set_password(password)
    user.cleartext_password = password

    user.save()

    return user


def create_service(service_class, person, date, town, kwargs_dict=None, is_by_phone=False):
    if not kwargs_dict:
        kwargs_dict = {}
    e = Encounter.objects.create(person=person, performed_on=date, where=town, is_by_phone=is_by_phone)
    service_kwargs = copy(kwargs_dict)
    service_kwargs.update({
        'encounter': e,
        'content_type': ContentType.objects.get_by_natural_key('services',
        service_class.__name__),
    })

    return service_class.objects.create(**service_kwargs)
