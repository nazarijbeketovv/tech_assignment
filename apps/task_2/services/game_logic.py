from django.db import transaction
from django.utils import timezone

from apps.task_2.models.game import LevelPrize, PlayerLevel, Prize


def assign_prize_to_player(player_id, level_id):
    try:
        # Используем транзакцию, чтобы избежать проблем с целостностью данных
        with transaction.atomic():
            player_level = PlayerLevel.objects.select_for_update().get(
                player__player_id=player_id, level_id=level_id
            )

            if not player_level.is_completed:
                raise ValueError("Level not completed yet")

            # Проверяем, если игрок уже получил приз
            if LevelPrize.objects.filter(
                level=player_level.level, received__isnull=False
            ).exists():
                raise ValueError("Prize already assigned")

            # Назначаем приз
            prize = Prize.objects.first()  # Здесь выбираем логически подходящий приз
            LevelPrize.objects.create(
                level=player_level.level, prize=prize, received=timezone.now()
            )

            return f"Prize {prize.title} assigned to player {player_id} for level {player_level.level.title}"

    except PlayerLevel.DoesNotExist:
        raise ValueError("Player or level not found")
    except Exception as e:
        raise ValueError(str(e))
