import csv
from django.test import TestCase
from django.utils import timezone
from ..models import Player, Level, PlayerLevel, Prize, LevelPrize
from ..utils import export_player_levels_to_csv


class ExportPlayerLevelsToCsvTestCase(TestCase):

    def setUp(self):
        # Создаем игрока, уровень и приз
        self.player = Player.objects.create(player_id="player_1")
        self.level = Level.objects.create(title="Level 1", order=1)
        self.prize = Prize.objects.create(title="Gold Medal")

        # Создаем связь игрока и уровня с завершенным уровнем
        self.player_level = PlayerLevel.objects.create(
            player=self.player,
            level=self.level,
            is_completed=True,
            completed=timezone.now(),
            score=100,
        )

        # Присваиваем приз
        LevelPrize.objects.create(
            level=self.level, prize=self.prize, received=timezone.now()
        )

    def _decode_streaming_content(self, streaming_content):
        """Метод для декодирования байтов в строки для корректного чтения CSV"""
        for chunk in streaming_content:
            yield chunk.decode("utf-8")

    def test_export_csv_success(self):
        # Тестируем успешную выгрузку данных в CSV
        response = export_player_levels_to_csv()

        # Декодируем содержимое ответа
        streaming_content = self._decode_streaming_content(response.streaming_content)

        # Проверяем корректность заголовков и данных
        csv_reader = csv.reader(streaming_content)
        header = next(csv_reader)

        self.assertEqual(header, ["player_id", "level", "is_completed", "prizes"])

        data = next(csv_reader)
        self.assertEqual(
            data, [self.player.player_id, self.level.title, "True", self.prize.title]
        )

    def test_export_csv_no_prizes(self):
        # Удаляем присвоенный приз
        LevelPrize.objects.all().delete()

        response = export_player_levels_to_csv()

        # Декодируем содержимое ответа
        streaming_content = self._decode_streaming_content(response.streaming_content)

        # Пропускаем заголовки
        csv_reader = csv.reader(streaming_content)
        next(csv_reader)  # Пропускаем первую строку с заголовками

        # Проверяем, что в выгрузке нет приза
        data = next(csv_reader)
        self.assertEqual(
            data, [self.player.player_id, self.level.title, "True", "No prize"]
        )

    def test_export_large_data(self):
        # Очищаем базу данных перед началом теста
        Player.objects.all().delete()
        Level.objects.all().delete()
        PlayerLevel.objects.all().delete()

        # Создаем 10000 записей
        for i in range(10000):
            player = Player.objects.create(player_id=f"player_{i}")
            level = Level.objects.create(title=f"Level {i}", order=i)
            PlayerLevel.objects.create(
                player=player,
                level=level,
                is_completed=True,
                completed=timezone.now(),
                score=i,
            )

        response = export_player_levels_to_csv()

        # Декодируем содержимое ответа
        streaming_content = self._decode_streaming_content(response.streaming_content)

        # Подсчитываем количество строк, включая заголовки
        csv_reader = csv.reader(streaming_content)
        rows_count = sum(1 for row in csv_reader)

        # Ожидаем 10000 записей + 1 строку заголовков
        self.assertEqual(rows_count, 10001)
