""" Events factories """
import datetime

import factory.fuzzy
import faker

from accounts.factories import AccountFactory
from events.models import Event

FAKE = faker.Factory.create()


class EventFactory(factory.DjangoModelFactory):
    """
    Event Factory on Sheparny
    """
    title = factory.LazyAttribute(lambda o: FAKE.word())  # pylint: disable=no-member
    description = factory.LazyAttribute(lambda o: FAKE.paragraph())  # pylint: disable=no-member
    created_by = factory.SubFactory(AccountFactory)
    date = factory.fuzzy.FuzzyDate(datetime.date(2018, 1, 1))

    class Meta:
        model = Event

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """ Add all the participants """
        participants = kwargs.pop('participants', [])
        obj = super()._create(model_class, *args, **kwargs)

        for participant in participants:
            obj.participants.add(participant)

        return obj
