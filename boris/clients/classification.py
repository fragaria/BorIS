# -*- coding: utf-8 -*-
'''
Created on 25.9.2011

@author: xaralis
'''
from model_utils import Choices

SEXES = Choices(
    (1, 'FEMALE', u'žena'),
    (2, 'MALE', u'muž')
)
APPLICATIONS = Choices(
    (1, 'IV', u'IV'),
    (2, 'NO_IV', 'neIV')
)
NATIONALITIES = Choices(
    (1, 'CZ', u'Česká republika'),
    (2, 'EU', u'Jiné - EU'),
    (3, 'NON_EU', u'Jiné - non-EU'),
    (4, 'UNKNOWN', u'Neznámo')
)
ETHNIC_ORIGINS = Choices(
    (1, 'NON_GYPSY', u'Ne-romská'),
    (2, 'GYPSY', u'Romská'),
    (3, 'NOT_MONITORED', u'Nesledováno')
)
LIVING_CONDITIONS = Choices(
    (1, 'ALONE', u'Sám'),
    (2, 'WITH_FAMILY', u'S rodiči/rodinou'),
    (3, 'WITH_FRIENDS', u'S přáteli'),
    (4, 'WITH_PARTNER', u'S partnerem'),
    (5, 'WITH_PARTNER_AND_CHILDREN', u'S partnerem a dítětem'),
    (6, 'ALONE_WITH_CHILDREN', u'Sám s dítětem')
)
ACCOMODATION_TYPES = Choices(
    (1, 'WITH_PARENTS', u'Doma (u rodičů)'),
    (2, 'OWN_FLAT', u'Vlastní byt (i pronajatý)'),
    (3, 'FOREIGN_FLAT', u'Cizí byt'),
    (4, 'PUBLIC_ACCOMODATION', u'Ubytovna'),
    (5, 'SQUAT', u'Squat'),
    (6, 'BARRACKS', u'Kasárna'),
    (7, 'HOMELESS', u'Bez domova, na ulici')
)
EMPLOYMENT_TYPES = Choices(
    (1, 'REGULAR', u'Pravidelné zam.'),
    (2, 'SCHOOL', u'Škola'),
    (3, 'OCCASIONAL_WORK', u'Příležitostná práce'),
    (4, 'REGISTERED_ON_EB', u'Registrován na ÚP'),
    (5, 'NO_EMPLOYMENT', u'Bez zaměstnání'),
    (6, 'STATE_SUPPORT', u'Dávky SZ')
)
EDUCATION_LEVELS = Choices(
    (1, 'BASIC', u'Základní'),
    (2, 'PRACTICAL_SECONDARY', u'Vyučen'),
    (3, 'SECONDARY', u'Střední s maturitou'),
    (4, 'HIGHER_PRACTICAL', u'Vyšší odborné'),
    (5, 'UNIVERSITY_GRADE', u'Vysokoškolské'),
    (6, 'BASIC_NOT_COMPLETED', u'Neukončené základní')
)
DRUG_APPLICATION_FREQUENCY = Choices(
    (1, 'LESS_THAN_3X_A_MONTH', u'méně než 3x měsíčně'),
    (2, 'ONCE_A_WEEK', u'1x týdně'),
    (3, 'ON_WEEKENDS', u'víkendově'),
    (4, 'EVERY_SECOND_DAY', u'obden'),
    (5, 'DAILY', u'denně'),
    (6, '2X_3X_A_DAY', u'2-3x denně'),
    (7, 'MORE_THAN_3X_A_DAY', u'více než 3x denně'),
    (8, 'NONE_FOR_MORE_THAN_6_MONTHS', u'neužita déle než 6 měsíců'),
    (9, 'NONE_FOR_LAST_6_MONTHS', u'neužita posledních 6 měsíců'),
    (10, 'NONE_FOR_LAST_3_MONTHS', u'neužita poslední 3 měsíce'),
    (11, 'NONE_FOR_LAST_1_MONTH', u'neužita v posledním měsíci')
)
DRUG_APPLICATION_TYPES = Choices(
    (1, 'VEIN_INJECTION', u'injekčně do žíly'),
    (2, 'MUSCLE_INJECTION', u'injekčně do svalu'),
    (3, 'ORAL', u'ústně'),
    (4, 'SNIFFING', u'sniff (šňupání)'),
    (5, 'SMOKING', u'kouření'),
    (6, 'INHALATION', u'inhalace')
)

PRIMARY_DRUG_APPLICATION_TYPES = Choices(
    (1, 'IV', u'intravenózní (IV)'),
    (2, 'NON_IV', u'jiná (neIV)'),
)

RISKY_BEHAVIOR_PERIODICITY = Choices(
        (1, 'NEVER', u'Nikdy'),
        (1, 'ONCE_BACK_THEN', u'Jednorázově v minulosti'),
        (1, 'OFTEN_BACK_THEN', u'Opakovaně v minulosti'),
        (1, 'ONCE_CURRENTLY', u'Jednorázově v současnosti'),
        (1, 'OFTEN_CURRENTLY', u'Opakovaně v současnosti'),
)

DISEASES = Choices(
    (1, 'HIV', u'HIV'),
    (2, 'VHA', u'VHA'),
    (3, 'VHB', u'VHB'),
    (4, 'VHC', u'VHC'),
)

DISEASE_TEST_RESULTS = Choices(
    (1, 'TESTED', u'Testován'),
    (2, 'NOT_TESTED', u'Netestován'),
    (3, 'RESULT_NOT_ACCLAIMED', u'Nevyzvedl výsledek'),
    (4, 'UNKNOWN', u'Neznámo')
)

