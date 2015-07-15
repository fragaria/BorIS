from django.core.management.base import NoArgsCommand, CommandError
from boris.reporting.management.install_views import install_views


class Command(NoArgsCommand):
    help = 'Reinstall reporting views'

    def handle_noargs(self, **options):
        install_views(None)
