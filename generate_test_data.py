from random import choice, randint, random
from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType

from boris.classification import SEXES, DRUG_APPLICATION_TYPES,\
        EMPLOYMENT_TYPES, EDUCATION_LEVELS, DISEASES
from boris.clients.models import Anonymous, Client, Town, District, Region,\
        Drug, Practitioner
from boris.services.models import Encounter, Service
from boris.services.models import HarmReduction, IncomeExamination,\
        InformationService, ContactWork, IndividualCounseling, Address,\
        PhoneCounseling, DiseaseTest

"""
Fills the database with the amount of data as expected in production.
The encounters (and services) are uniformly spread throughout the whole year.

Usage: set the desired constants, import the whole script from manage.py shell
and then run reset() and/or generate().
"""

CLIENT_CNT = 400
PRACTITIONER_CNT = 20
TOWN_CNT = 14
DISTRICT_CNT = 6
REGION_CNT = 3
CLIENT_ENCOUNTERS_CNT = 4000
ANONYMOUS_ENCOUNTERS_CNT = 1000
PRACTITIONER_ENCOUNTERS_CNT = 1000
BASE_YEAR = datetime(year=2011, month=1, day=1)
SERVICE_CNT = 1000 # number of times each service is performed

def reset():
    print "Cleaning up the database..."
    Drug.objects.all().delete()
    Client.objects.all().delete()
    Town.objects.all().delete()
    District.objects.all().delete()
    Region.objects.all().delete()
    Encounter.objects.all().delete()
    Service.objects.all().delete()
    Practitioner.objects.all().delete()

def generate():
    print "Generating Regions..."
    for i in xrange(1, REGION_CNT + 1):
        fields = {
            "title": 'Region%i' % i,
        }
        r = Region(**fields)
        r.save()

    print "Generating Districts..."
    regions = list(Region.objects.all())
    for i in xrange(1, DISTRICT_CNT + 1):
        fields = {
            "title": 'District%i' % i,
            "region": choice(regions),
        }
        d = District(**fields)
        d.save()

    print "Generating Towns..."
    districts = list(District.objects.all())
    for i in xrange(1, TOWN_CNT + 1):
        fields = {
            "title": 'Town%i' % i,
            "district": choice(districts),
        }
        t = Town(**fields)
        t.save()

    print "Generating Clients..."
    drug = Drug.objects.create(title='hero')
    towns = list(Town.objects.all())
    ctype = ContentType.objects.get_by_natural_key('clients', 'client')
    for i in xrange(1, CLIENT_CNT + 1):
        client_drug = choice([None, drug])
        fields = {
            "code": "CODE%s" % i,
            "sex": choice([SEXES.FEMALE, SEXES.MALE]),
            "town": choice(towns),
            "title": 'Client%i' % i,
            "content_type": ctype,
            "primary_drug": client_drug,
            "primary_drug_usage": choice([
                DRUG_APPLICATION_TYPES.VEIN_INJECTION,
                DRUG_APPLICATION_TYPES.UNKNOWN,
            ]),
        }
        c = Client(**fields)
        c.save()

    print "Generating Practitioners..."
    towns = list(Town.objects.all())
    ctype = ContentType.objects.get_by_natural_key('clients', 'practitioner')
    for i in xrange(1, PRACTITIONER_CNT + 1):
        fields = {
            "sex": choice([SEXES.FEMALE, SEXES.MALE]),
            "town": choice(towns),
            "last_name": 'sroubek%i' % i,
            "content_type": ctype,
        }
        p = Practitioner(**fields)
        p.save()

    clients = list(Client.objects.all())
    anonyms = list(Anonymous.objects.all())
    practitioners = list(Practitioner.objects.all())
    days = [BASE_YEAR + timedelta(days=i) for i in xrange(1, 350)]

    print "Generating Encounters..."
    client_encounters = []
    for i in xrange(1, CLIENT_ENCOUNTERS_CNT + 1):
        fields = {
            "person": choice(clients),
            "performed_on": choice(days),
            "where": choice(towns),
        }
        e = Encounter(**fields)
        e.save()
        client_encounters.append(e)

    anonymous_encounters = []
    for i in xrange(1, ANONYMOUS_ENCOUNTERS_CNT + 1):
        fields = {
            "person": choice(anonyms),
            "performed_on": choice(days),
            "where": choice(towns),
        }
        e = Encounter(**fields)
        e.save()
        anonymous_encounters.append(e)
    person_encounters = client_encounters + anonymous_encounters

    practitioner_encounters = []
    for i in xrange(1, PRACTITIONER_ENCOUNTERS_CNT + 1):
        fields = {
            "person": choice(practitioners),
            "performed_on": choice(days),
            "where": choice(towns),
        }
        e = Encounter(**fields)
        e.save()
        practitioner_encounters.append(e)

    person_encounters = client_encounters + anonymous_encounters + practitioner_encounters

    print "Generating Services..."
    ctypes = {}
    for model in ('harmreduction', 'incomeexamination',
            'informationservice', 'contactwork', 'individualcounseling',
            'phonecounseling', 'address', 'diseasetest'):
        ctypes[model] = ContentType.objects.get_by_natural_key('services', model)
    for i in xrange(1, SERVICE_CNT + 1):
        fields = {
            "encounter": choice(client_encounters),
            "content_type": ctypes['harmreduction'],
            "in_count": randint(1, 100),
            "out_count": randint(1, 100),
        }
        s = HarmReduction(**fields)
        s.save()

        fields = {
            "content_type": ctypes['incomeexamination'],
            "encounter": choice(client_encounters),
        }
        s = IncomeExamination(**fields)
        s.save()

        fields = {
            "content_type": ctypes['contactwork'],
            "encounter": choice(client_encounters),
        }
        s = ContactWork(**fields)
        s.save()

        fields = {
            "content_type": ctypes['informationservice'],
            "safe_usage": choice([False, True]),
            "safe_sex": choice([False, True]),
            "medical": choice([False, True]),
            "socio_legal": choice([False, True]),
            "cure_possibilities": choice([False, True]),
            "literature": choice([False, True]),
            "other": choice([False, True]),
            "encounter": choice(person_encounters),
        }
        s = InformationService(**fields)
        s.save()

        fields = {
            "content_type": ctypes['individualcounseling'],
            "encounter": choice(client_encounters),
        }
        s = IndividualCounseling(**fields)
        s.save()

        fields = {
            "content_type": ctypes['address'],
            "encounter": choice(person_encounters),
        }
        s = Address(**fields)
        s.save()

        fields = {
            "content_type": ctypes['phonecounseling'],
            "encounter": choice(person_encounters),
        }
        s = PhoneCounseling(**fields)
        s.save()

        fields = {
            "content_type": ctypes['diseasetest'],
            "encounter": choice(person_encounters),
            "disease": choice(list(DISEASES))[0],
        }
        s = DiseaseTest(**fields)
        s.save()
