from boris.reporting.core import BaseReport


class BaseImpact(BaseReport):
    template_path = 'impact'

    def get_filename(self):
        return 'impact.xls'
