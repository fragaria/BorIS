from django.db.models import Model
from boris.clients.models import Client
from boris.services.models import Service

__author__ = 'ondrej'


class DummyServiceClass(Service):
    class Meta:
        app_label = 'services'
        proxy = True
        # db_table = 'app_largetable'  # try combining managed=False and db_table name
        # also SOUTH_TESTS_MIGRATE=False a app_label


    class Options:
        description_template = 'services/desc/aaa.html'
        is_available = lambda client: True if client == 1 else False


class ModelDummy(Client):
    class Meta:
        app_label = 'services'
        proxy = True


class DummyLimitedServiceClass(Service):
    class Meta:
        app_label = 'services'
        proxy = True

    class Options:
        limited_to = ('Client',)
        is_available = lambda client: not hasattr(client, 'failme')


class Dummy1(Service):
    class Meta:
        app_label = 'services'
        proxy = True

    class Options:
        is_available = lambda client: False


class Dummy2(Service):
    class Meta:
        app_label = 'services'
        proxy = True

    class Options:
        is_available = lambda client: True