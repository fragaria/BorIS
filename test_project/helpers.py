from django.contrib.auth.models import User

from boris.clients.models import Client, Town, Region, District
from boris.clients.classification import SEXES
from django.utils.functional import curry

def get_testing_string_enum(ModelClass, title, *args, **kwargs):
    return ModelClass.objects.create(title=title, **kwargs)

get_testing_region = curry(get_testing_string_enum, Region, 'Stredocesky')
get_testing_district = curry(get_testing_string_enum, District, 'Rakovnik', region=get_testing_region())
get_testing_town = curry(get_testing_string_enum, Town, 'Rakovnik', district=get_testing_district())

def get_testing_client(code='borivoj22'):
    client_data = {
         'code': code,
         'sex': SEXES.MALE,
         'birthdate': '1980-10-10',
         'town': get_testing_town(),
    }
    
    return Client.objects.create(**client_data)


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

