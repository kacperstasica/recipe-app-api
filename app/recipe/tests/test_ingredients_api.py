from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from core.models import Ingredient
from users.factories import UserFactory, IngredientFactory

from recipe.serializers import IngredientSerializer


class PublicIngredientsApiTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.INGREDIENTS_URL = reverse('recipe:ingredient-list')

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(self.INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(APITestCase):
    """Test the private ingredients API"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.auth_token = Token.objects.create(user=cls.user)
        cls.INGREDIENTS_URL = reverse('recipe:ingredient-list')

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.auth_token.key
        )

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        IngredientFactory(user=self.user, name='Kale')
        IngredientFactory(user=self.user, name='Salt')

        res = self.client.get(self.INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the auth user are returned"""
        user2 = UserFactory()
        IngredientFactory(user=user2, name='Vinegar')
        ingredient = IngredientFactory(user=self.user, name='Tumeric')

        res = self.client.get(self.INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
