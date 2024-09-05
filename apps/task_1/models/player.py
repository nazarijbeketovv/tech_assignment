from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authentication import get_user_model


class Player(models.Model):
    """
    Модель игрока. Хранит информацию о пользователе, его баллах и первой дате входа.
    """

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="player_profile"
    )
    points = models.IntegerField(default=0, verbose_name="Очки")
    first_login = models.DateTimeField(
        null=True, blank=True, verbose_name="Первый вход"
    )
    last_login = models.DateTimeField(
        null=True, blank=True, verbose_name="Последний вход"
    )
    

    def update_login(self):
        """
        Обновление информации о первом и последнем входе игрока.
        """
        now = timezone.now()
        if not self.first_login:
            self.first_login = now
        self.last_login = now
        self.save()

    def add_points(self, points):
        """
        Метод для добавления очков игроку.
        """
        self.points += points
        self.save()

    def deduct_points(self, points):
        """
        Метод для снятия очков у игрока.
        """
        self.points = max(0, self.points - points)
        self.save()

    def __str__(self):
        return f"Player: {self.user.username}, Points: {self.points}"


@receiver(post_save, sender=get_user_model())
def create_player_profile(sender, instance, created, **kwargs):
    """
    Сигнал для автоматического создания профиля игрока при создании пользователя.
    """
    if created:
        Player.objects.create(user=instance)


class Boost(models.Model):
    """
    Модель буста. Хранит информацию о типе и длительности буста.
    """

    BOOST_TYPE_CHOICES = (
        ("speed", "Ускорение"),
        ("strength", "Сила"),
        ("defense", "Защита"),
    )

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="boosts")
    boost_type = models.CharField(
        max_length=20, choices=BOOST_TYPE_CHOICES, verbose_name="Тип буста"
    )
    duration = models.DurationField(verbose_name="Длительность буста")
    activated_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время активации"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def check_activation_status(self):
        """
        Проверяет и обновляет статус активности буста.
        """
        if self.is_active and not self.is_boost_active():
            self.is_active = False
            self.save()

    def is_boost_active(self):
        """
        Проверяет, активен ли буст.
        """
        now = timezone.now()
        return now < self.activated_at + self.duration

    def __str__(self):
        return f"{self.get_boost_type_display()} for {self.player.user.username} (Duration: {self.duration})"
