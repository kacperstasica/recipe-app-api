from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Tag, Ingredient
from users.factories import UserFactory


def sample_user(email='test@wp.pl', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()

    def test_create_user_with_email_successfull(self):
        email = 'test@laboratorium.ee'
        password = 'Testpass123'
        user = UserFactory(
            email=email,
        )
        user.set_password(password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'test@LABORATORIUM.EE'
        user = get_user_model().objects.create_user(
            email,
            'test123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                'test123'
            )

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@laboratoirum.ee',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag str representation"""
        tag = Tag.objects.create(
            user=sample_user(),
            name='Vegan',
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string repr"""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='Cucumber',
        )

        self.assertEqual(str(ingredient), ingredient.name)
