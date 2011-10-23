'''
Created on 22.10.2011

@author: xaralis
'''
from djangosanetesting.cases import UnitTestCase
from boris.services.models.core import ClientService

class TestClientServiceMetaClass(UnitTestCase):
    def test_clientservice_subclass_is_registered_after_declaration(self):
        class DummyServiceClass(ClientService):
            pass
        
        self.assert_true(DummyServiceClass in ClientService.registered_services)
        
    def test_subclassing_clientservice_adds_service_meta_class(self):
        class DummyServiceClass(ClientService):
            pass
        
        self.assert_true(hasattr(DummyServiceClass, 'service'))
        service_meta = DummyServiceClass.service
        
        self.assert_true(hasattr(service_meta, 'title'))
        self.assert_true(hasattr(service_meta, 'description_template'))
        self.assert_true(hasattr(service_meta, 'available'))
        