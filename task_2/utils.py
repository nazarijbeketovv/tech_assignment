from django.http import StreamingHttpResponse
from .models import LevelPrize, PlayerLevel


class Echo:
    """Класс для эмуляции записи строки в StreamingHttpResponse"""

    def write(self, value):
        return value


def export_player_levels_to_csv():
    # Генератор для стриминга данных
    def generate():
        # Добавляем заголовки
        yield ["player_id", "level", "is_completed", "prizes"]

        # Получаем данные для выгрузки
        for player_level in PlayerLevel.objects.select_related("player", "level"):
            player_id = player_level.player.player_id
            level_title = player_level.level.title
            is_completed = player_level.is_completed
            # Проверяем, получен ли приз
            prize = (
                LevelPrize.objects.filter(level=player_level.level).first().prize.title
                if LevelPrize.objects.filter(level=player_level.level).exists()
                else "No prize"
            )
            yield [player_id, level_title, str(is_completed), prize]

    # Создаем StreamingHttpResponse
    response = StreamingHttpResponse(
        (",".join(row) + "\n" for row in generate()), content_type="text/csv"
    )
    response["Content-Disposition"] = 'attachment; filename="player_levels.csv"'
    return response
