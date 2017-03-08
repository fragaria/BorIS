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
    (6, 'ALONE_WITH_CHILDREN', u'Sám s dítětem'),
    (7, 'UNKNOWN', u'Není známo')
)
ACCOMODATION_TYPES = Choices(
    (1, 'WITH_PARENTS', u'Doma (u rodičů)'),
    (2, 'OWN_FLAT', u'Vlastní byt (i pronajatý)'),
    (3, 'FOREIGN_FLAT', u'Cizí byt'),
    (4, 'PUBLIC_ACCOMODATION', u'Ubytovna'),
    (5, 'SQUAT', u'Squat'),
    (6, 'BARRACKS', u'Kasárna'),
    (7, 'HOMELESS', u'Bez domova, na ulici'),
    (8, 'UNKNOWN', u'Není známo')
)
EMPLOYMENT_TYPES = Choices(
    (1, 'REGULAR', u'Pravidelné zam.'),
    (2, 'SCHOOL', u'Škola'),
    (3, 'OCCASIONAL_WORK', u'Příležitostná práce'),
    (4, 'REGISTERED_ON_EB', u'Registrován na ÚP'),
    (5, 'NO_EMPLOYMENT', u'Bez zaměstnání'),
    (6, 'STATE_SUPPORT', u'Dávky SZ'),
    (8, 'UNKNOWN', u'Není známo')
)
EDUCATION_LEVELS = Choices(
    (1, 'BASIC', u'Základní'),
    (2, 'PRACTICAL_SECONDARY', u'Vyučen'),
    (3, 'SECONDARY', u'Střední s maturitou'),
    (4, 'HIGHER_PRACTICAL', u'Vyšší odborné'),
    (5, 'UNIVERSITY_GRADE', u'Vysokoškolské'),
    (6, 'BASIC_NOT_COMPLETED', u'Neukončené základní'),
    (7, 'UNKNOWN', u'Není známo')
)
DRUGS = Choices( # (Numbers reflect the old drug ids.)
    (3, 'METHAMPHETAMINE', u'Pervitin, jiné amfetaminy'),
    (4, 'SUBUTEX_LEGAL', u'Subutex, Ravata, Buprenorphine alkaloid - legálně'),
    (5, 'TOBACCO', u'Tabák'),
    (8, 'THC', u'THC'),
    (9, 'ECSTASY', u'Extáze'),
    (10, 'DESIGNER_DRUGS', u'Designer drugs'),
    (11, 'HEROIN', u'Heroin'),
    (12, 'BRAUN', u'Braun a jiné opiáty'),
    (13, 'RAW_OPIUM', u'Surové opium'),
    (14, 'SUBUTEX_ILLEGAL', u'Subutex, Ravata, Buprenorphine alkaloid - ilegálně'),
    (16, 'ALCOHOL', u'Alkohol',),
    (17, 'INHALER_DRUGS', u'Inhalační látky, ředidla'),
    (18, 'MEDICAMENTS', u'Medikamenty'),
    (19, 'METHADONE', u'Metadon'),
    (20, 'COCAINE', u'Kokain, crack'),
    (21, 'SUBOXONE', u'Suboxone'),
    (22, 'VENDAL', u'Vendal'),
    (23, 'LSD', u'LSD'),
    (24, 'PSYLOCIBE', u'Lysohlávky'),
    (25, 'UNKNOWN', u'Neznámo'),
    (26, 'PATHOLOGICAL_GAMBLING', u'Patologické hráčství'),
    (27, 'OTHER_NON_SUBSTANCE_ADDICTION', u'Jiná nelátková závislost'),
)

# Disable `application`, `first_try_application` and `primary_drug_usage` fields for these drugs
NON_APPLICATION_DRUGS = ['26', '27']

DRUG_APPLICATION_FREQUENCY = Choices(
    (1, 'LESS_THAN_3X_A_MONTH', u'méně než 3x měsíčně'),
    (2, 'ONCE_A_WEEK', u'1x týdně'),
    (3, 'ON_WEEKENDS', u'víkendově'),
    (4, 'EVERY_SECOND_DAY', u'obden'),
    (5, 'DAILY', u'denně'),
    (6, '2X_3X_A_DAY', u'2-3x denně'),
    (7, 'MORE_THAN_3X_A_DAY', u'více než 3x denně'),
    (8, 'NONE_FOR_MORE_THAN_6_MONTHS', u'neužita déle než 6 měsíců'),
#    (9, 'NONE_FOR_LAST_6_MONTHS', u'neužita posledních 6 měsíců'),  # Feature 103
    (10, 'NONE_FOR_LAST_3_MONTHS', u'neužita poslední 3 měsíce'),
    (11, 'NONE_FOR_LAST_1_MONTH', u'neužita v posledním měsíci'),
    (12, 'UNKNOWN', u'Není známo')
)
DRUG_APPLICATION_TYPES = Choices(
    (1, 'VEIN_INJECTION', u'injekčně do žíly'),
    (2, 'MUSCLE_INJECTION', u'injekčně do svalu'),
    (3, 'ORAL', u'ústně'),
    (4, 'SNIFFING', u'sniff (šňupání)'),
    (5, 'SMOKING', u'kouření'),
    (6, 'INHALATION', u'inhalace'),
    (7, 'UNKNOWN', u'Není známo')
)

RISKY_BEHAVIOR_KIND = Choices(
    (1, 'EQUIPMENT_SHARING', u'Sdílení náčiní'),
    (2, 'SEX_WITHOUT_PROTECTION', u'Nechráněný sex'),
    (3, 'SYRINGE_SHARING', u'Sdílení jehel'),
    (4, 'INTRAVENOUS_APPLICATION', u'Nitrožilní aplikace'),
    (5, 'RISKY_APPLICATION', u'Riziková aplikace'),
    (6, 'OVERDOSING', u'Předávkování'),
    (7, 'HEALTH_COMPLICATIONS', u'Zdravotní komplikace')
)

RISKY_BEHAVIOR_PERIODICITY = Choices(
    (1, 'NEVER', u'Nikdy'),
    (2, 'ONCE', u'Jednorázově'),
    (3, 'OFTEN', u'Opakovaně '),
    (4, 'UNKNOWN', u'Není známo')
)

DISEASES = Choices(
    (1, 'HIV', u'HIV'),
    (2, 'VHA', u'VHA'),
    (3, 'VHB', u'VHB'),
    (4, 'VHC', u'VHC'),
    (5, 'SYFILIS', u'Syfilis'),
)

DISEASE_TEST_RESULTS = Choices(
    (0, 'UNKNOWN', u'Neznámo, zda testován'),
    (1, 'TESTED_POSITIVE', u'Testován - pozitivní'),
    (2, 'TESTED_NEGATIVE', u'Testován - negativní'),
	(3, 'TESTED_UNKNOWN', u'Testován - výsledek neznámý'),
    (4, 'NOT_TESTED', u'Nikdy netestován'),
    (5, 'RESULT_NOT_ACCLAIMED', u'Nevyzvedl výsledek'),
)

DISEASE_TEST_SIGN = Choices(
    ('p', 'POSITIVE', u'Pozitivní'),
    ('n', 'NEGATIVE', u'Negativní'),
    ('r', 'REACTIVE', u'Reaktivní'),
    ('i', 'INCONCLUSIVE', u'Test neprůkazný')
)

ANONYMOUS_TYPES = Choices(
    (1, 'NON_USER', u'neuživatel'),
    (2, 'NON_IV', u'neIV'),
    (3, 'IV', u'IV'),
    (4, 'NON_USER_PARENT', u'rodič'),
    (5, 'THC', u'THC')
)

