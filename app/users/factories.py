import factory.fuzzy

from core.models import User, Ingredient


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: f'test-{n}@wp.pl')

    class Meta:
        model = User


class IngredientFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Ingredient
