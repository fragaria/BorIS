from django.contrib.auth.models import User
from django.utils.functional import curry
from django.contrib.contenttypes.models import ContentType

from boris.clients.models import Client, Town, Region, District, Drug, Practitioner
from boris.classification import SEXES


def get_testing_string_enum(ModelClass, title, *args, **kwargs):
    return ModelClass.objects.create(title=title, **kwargs)

get_testing_region = curry(get_testing_string_enum, Region, 'Stredocesky')
get_testing_district = curry(get_testing_string_enum, District, 'Rakovnik', region=get_testing_region())
get_testing_town = curry(get_testing_string_enum, Town, 'Rakovnik', district=get_testing_district())
get_testing_drug = curry(get_testing_string_enum, Drug, 'Piko')

def get_testing_client(code='borivoj22', cdata=None):
    client_data = {
         'code': code,
         'sex': SEXES.MALE,
         'birthdate': '1980-10-10',
         'town': get_testing_town(),
         'content_type': ContentType.objects.get_for_model(Client)
    }

    if cdata:
        client_data.update(cdata)

    return Client.objects.create(**client_data)

def get_testing_practitioner(last_name='Sroubek'):
    practitioner_data = {
         'last_name': last_name,
         'sex': SEXES.MALE,
         'town': get_testing_town(),
         'content_type': ContentType.objects.get_for_model(Practitioner)
    }

    return Practitioner.objects.create(**practitioner_data)

def get_testing_user(username='strachkvas'):
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

