from djangosanetesting.cases import HttpTestCase

from django.core.urlresolvers import reverse

from boris.clients.models import ClientNote

from test_project.helpers import get_testing_user, get_testing_client


class TestClientNote(HttpTestCase):

   def setUp(self):

       self.my_client = get_testing_client()
       self.user = get_testing_user()


   def test_add_ok(self):
       self.client.login(username=self.user.username, password=self.user.cleartext_password)
       res = self.client.post(reverse('admin:clients_add_note', kwargs={'object_id': self.my_client.pk}),
           data = {'text': 'Note text.'},
           HTTP_X_REQUESTED_WITH='XMLHttpRequest'
       )

       self.assert_equals(200, res.status_code)


   def test_add_actually_adds(self):

       self.assert_equals(0, ClientNote.objects.count())
       self.client.login(username=self.user.username, password=self.user.cleartext_password)
       for i in range(0, 10):
           self.client.post(reverse('admin:clients_add_note', kwargs={'object_id': self.my_client.pk}),
               data = {'text': 'Note text.'},
               HTTP_X_REQUESTED_WITH='XMLHttpRequest'
           )
       self.assert_equals(10, ClientNote.objects.count())


   def test_restricted_access(self):
       # login ommitted
       self.assert_equals(0, ClientNote.objects.count())
       self.client.post(reverse('admin:clients_add_note', kwargs={'object_id': self.my_client.pk}),
           data = {'text': 'Note text.'},
           HTTP_X_REQUESTED_WITH='XMLHttpRequest'
       )
       self.assert_equals(0, ClientNote.objects.count())

