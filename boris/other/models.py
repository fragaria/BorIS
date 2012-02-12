from django.db import models
from django.utils.translation import ugettext_lazy as _

from fragapy.common.models.adminlink import AdminLinkMixin

class SyringeCollection(models.Model, AdminLinkMixin):
    '''
    Simple model to record collecting of syringes
    '''
    count = models.PositiveIntegerField(verbose_name=_('how much'))
    persons = models.ManyToManyField('auth.User', verbose_name=_('who'))
    town = models.ForeignKey('clients.Town', related_name='+', verbose_name=_('town'))
    date = models.DateField(verbose_name=_('when'))
    location = models.CharField(max_length=255, verbose_name=_('location'),
        blank=True)

    class Meta:
        verbose_name = _('syringe collection')
        verbose_name_plural = _('syringe collections')

    def __unicode__(self):
        return u'%s - %s (%d Ks %s)' % (','.join([unicode(p) for p in self.persons.all()]), self.date, self.count, self.location)
