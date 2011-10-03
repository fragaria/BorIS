from django.contrib.auth.models import User

from boris.clients.models import Client, Town
from boris.clients.classification import SEXES


def get_testing_client(code='borivoj22'):
       town = Town.objects.create(title='Rakovnik') # TODO: move into a test fixture

       client_data = {
            'code': code,
            'sex': SEXES.MALE,
            'birthdate': '1980-10-10',
            'town': town,
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

