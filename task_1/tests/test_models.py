from django.test import TestCase
from rest_framework.authentication import get_user_model

from ..models import Player


class PlayerModelTests(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.player = self.user.player_profile

    def test_player_profile_creation(self):
        """
        Проверка автоматического создания профиля игрока.
        """
        # Проверяем, что профиль игрока существует
        self.assertIsInstance(self.player, Player)
        # Проверяем, что профиль связан с правильным пользователем
        self.assertEqual(self.player.user, self.user)

    def test_update_login(self):
        """
        Проверка обновления первого и последнего входа.
        """
        self.player.update_login()
        self.assertIsNotNone(self.player.first_login)
        self.assertEqual(self.player.first_login, self.player.last_login)

        # Обновим вход
        previous_login = self.player.last_login
        self.player.update_login()
        self.assertGreater(self.player.last_login, previous_login)

    def test_add_and_deduct_points(self):
        """
        Проверка начисления и снятия очков.
        """
        self.player.add_points(10)
        self.assertEqual(self.player.points, 10)

        self.player.deduct_points(5)
        self.assertEqual(self.player.points, 5)

        # Проверка, что очки не уходят в минус
        self.player.deduct_points(10)
        self.assertEqual(self.player.points, 0)
