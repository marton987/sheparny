""" Accounts factories """
import factory
import faker
from accounts.models import Account

FAKE = faker.Factory.create()


class AccountFactory(factory.DjangoModelFactory):
    """
    Account Factory on Sheparny
    """
    email = factory.LazyAttribute(lambda o: FAKE.email())  # pylint: disable=no-member
    username = factory.LazyAttribute(lambda o: FAKE.first_name())  # pylint: disable=no-member
    password = 'password'
    is_active = True

    class Meta:
        model = Account
