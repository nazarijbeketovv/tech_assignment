from django.test import TestCase
from django.utils import timezone
from ..models import Player, Level, PlayerLevel, Prize, LevelPrize
from ..game_logic import assign_prize_to_player


class PrizeAssignmentTestCase(TestCase):

    def setUp(self):
        # Создаем игрока, уровень и приз
        self.player = Player.objects.create(player_id="player_1")
        self.level = Level.objects.create(title="Level 1", order=1)
        self.prize = Prize.objects.create(title="Gold Medal")

        # Создаем связь игрока и уровня
        self.player_level = PlayerLevel.objects.create(
            player=self.player,
            level=self.level,
            is_completed=True,
            completed=timezone.now(),
            score=100,
        )

    def test_prize_assignment_success(self):
        # Тест успешного присвоения приза
        response = assign_prize_to_player(self.player.player_id, self.level.id)
        self.assertIn("Prize Gold Medal assigned", response)

        # Проверяем, что приз действительно присвоен
        level_prize = LevelPrize.objects.filter(level=self.level).first()
        self.assertIsNotNone(level_prize)
        self.assertEqual(level_prize.prize, self.prize)

    def test_prize_already_assigned(self):
        # Присваиваем приз один раз
        LevelPrize.objects.create(
            level=self.level, prize=self.prize, received=timezone.now()
        )

        # Пробуем присвоить еще раз
        with self.assertRaises(ValueError):
            assign_prize_to_player(self.player.player_id, self.level.id)

    def test_level_not_completed(self):
        # Изменяем статус уровня на не завершенный
        self.player_level.is_completed = False
        self.player_level.save()

        # Ожидаем ошибку, так как уровень не завершен
        with self.assertRaises(ValueError):
            assign_prize_to_player(self.player.player_id, self.level.id)

    def test_player_or_level_not_found(self):
        # Пробуем присвоить приз несуществующему игроку
        with self.assertRaises(ValueError):
            assign_prize_to_player("invalid_player", self.level.id)
