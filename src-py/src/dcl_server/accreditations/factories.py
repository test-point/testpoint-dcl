import factory
from django.contrib.auth import get_user_model

from .models import AccreditedParty


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: 'john_%s' % n)


class AccreditedPartyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccreditedParty

    service_provider_id = factory.Sequence(lambda n: 'serviceprovider-%s' % n)
    trading_name = factory.Sequence(lambda n: 'Trading Name %s' % n)
    contact_email = factory.Sequence(lambda n: 'contact%s@email.org.lalala' % n)
    registration_url = factory.Sequence(lambda n: 'https://registration-%s.testpoint.io/' % n)
    dcl_host = factory.Sequence(lambda n: 'dcl-%s.testpoint.io' % n)

    accreditation_status = AccreditedParty.STATUS_ACCR
