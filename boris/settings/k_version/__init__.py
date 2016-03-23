# -*- encoding: utf8 -*-

from .. import *

ACTIVE_MODULES += ['k']

UTILITY_WORK_CHOICES[2] = ('mf', 'MEDICAL_FACILITY', u'3) Pobytová léčba')
UTILITY_WORK_CHOICES.insert(-1, ('amb', 'AMBULANT_TREATMENT', u'10) Ambulantní léčba'))
