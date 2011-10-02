from djangosanetesting.cases import HttpTestCase

from django.core.urlresolvers import reverse

#from boris.clients.models import Client, ClientNote, Town
from boris.clients.models import Client, Town
from boris.clients.classification import SEXES


class TestClientNote(HttpTestCase):

   def setUp(self):
       town = Town.objects.create(title='Rakovnik') # TODO: move into a test fixture

       client_data = { # TODO: move into a test helper
            'code': 'abcdef',
            'sex': SEXES.MALE,
            'birthdate': '1980-10-10',
            'town': town,
       }

       # self.client is the http client
       self.my_client = Client(**client_data)
       self.my_client.save()


   def test_add_ok(self):
       res = self.client.post(reverse('admin:clients_add_note', kwargs={'object_id': self.my_client.pk}),
           data = {'text': 'Note text.'},
           HTTP_X_REQUESTED_WITH='XMLHttpRequest'
       )

       self.assert_equals(200, res.status_code)


   def test_add_actually_adds(self):
       # TODO
       pass

