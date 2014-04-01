from django.db.models import Model
from boris.services.models import Service

__author__ = 'ondrej'

class DummyServiceClass(Service):
    class Meta:
        app_label = 'services'

class ModelDummy(Model):
    class Meta:
        app_label = 'services'

