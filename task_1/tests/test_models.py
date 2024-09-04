from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from ..models import Player, Boost


class PlayerModelTests(TestCase):
    """Тесты для модели игрока:
    1. Создание игрока.
    2. Проверка автоматического создания профиля игрока.
    3. Провека обновления последнего входа игрока.
    4. Проверка добавления и снятия очков игрока.
    """

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
        self.assertIsInstance(self.player, Player)
        self.assertEqual(self.player.user, self.user)

    def test_update_login(self):
        """
        Проверка обновления первого и последнего входа.
        """
        # Устанавливаем начальное время
        initial_time = timezone.now()
        self.player.first_login = initial_time
        self.player.last_login = initial_time
        self.player.save()

        # Увеличиваем время на одну секунду
        new_time = initial_time + timedelta(seconds=1)

        # Обновляем время вручную
        self.player.last_login = new_time
        self.player.save()

        # Проверяем, что время обновилось
        self.assertEqual(self.player.first_login, initial_time)
        self.assertGreater(self.player.last_login, initial_time)

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


class BoostModelTests(TestCase):
    """Тесты для модели буста:
    1. Создание буста и его активация.
    2. Проверка деактивации буста после окончания срока действия.
    """

    def setUp(self):
        # Создаем пользователя и игрока
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.player = self.user.player_profile

    def test_boost_creation_and_activation(self):
        """
        Проверка создания буста и его активации.
        """
        boost = Boost.objects.create(
            player=self.player, boost_type="speed", duration=timedelta(hours=1)
        )
        self.assertTrue(boost.is_active)
        self.assertTrue(boost.is_boost_active())

    def test_boost_deactivation(self):
        """
        Проверка деактивации буста после окончания срока действия.
        """
        boost = Boost.objects.create(
            player=self.player, boost_type="strength", duration=timedelta(seconds=1)
        )
        self.assertTrue(boost.is_boost_active())

        self._simulate_time_passing(seconds=2)

        boost.check_activation_status()
        self.assertFalse(boost.is_boost_active())
        self.assertFalse(boost.is_active)

    def _simulate_time_passing(self, seconds):
        """
        Вспомогательная функция для симуляции прохождения времени.
        """
        future_time = timezone.now() + timedelta(seconds=seconds)
        timezone.now = lambda: future_time
