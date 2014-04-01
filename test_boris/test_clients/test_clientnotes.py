from django.test import TestCase
from nose import tools
from django.core.urlresolvers import reverse

from boris.clients.models import ClientNote
from test_boris.helpers import get_tst_usr, get_tst_client


class TestClientNote(TestCase):
    def setUp(self):
        self.my_client = get_tst_client()
        self.user = get_tst_usr()

    def post_note(self):
        return self.client.post(reverse('admin:clients_add_note'),
                                data={
                                    'text': u'Note text.',
                                    'client': self.my_client.pk,
                                    'datetime_0': u'10.10.2010',
                                    'datetime_1': u'10:10',
                                },
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                                )

    def test_add_ok(self):
        self.client.login(username=self.user.username, password=self.user.cleartext_password)
        res = self.post_note()

        tools.assert_equals(200, res.status_code)

    def test_add_actually_adds(self):
        tools.assert_equals(0, ClientNote.objects.count())
        self.client.login(username=self.user.username,
                          password=self.user.cleartext_password)
        for i in range(0, 10):
            self.post_note()
        tools.assert_equals(10, ClientNote.objects.count())

    def test_restricted_access(self):
        # login ommitted
        tools.assert_equals(0, ClientNote.objects.count())
        self.post_note()

        tools.assert_equals(0, ClientNote.objects.count())

