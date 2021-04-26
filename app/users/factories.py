import factory.fuzzy

from core.models import User


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: f'test-{n}@wp.pl')

    class Meta:
        model = User
