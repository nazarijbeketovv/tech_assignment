from django.contrib import admin
from .models import Player, Level, Prize, PlayerLevel, LevelPrize


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "player_id")
    search_fields = ("player_id",)
    ordering = ("id",)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "order")
    search_fields = ("title",)
    list_filter = ("order",)
    ordering = ("order",)


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)
    ordering = ("title",)


class LevelInline(admin.TabularInline):
    model = PlayerLevel
    extra = 1
    fields = ("level", "completed", "is_completed", "score")
    readonly_fields = ("completed",)


@admin.register(PlayerLevel)
class PlayerLevelAdmin(admin.ModelAdmin):
    list_display = ("player", "level", "completed", "is_completed", "score")
    search_fields = ("player__player_id", "level__title")
    list_filter = ("is_completed", "level")
    ordering = ("-completed", "score")


class LevelPrizeInline(admin.TabularInline):
    model = LevelPrize
    extra = 1
    fields = ("prize", "received")
    readonly_fields = ("received",)


@admin.register(LevelPrize)
class LevelPrizeAdmin(admin.ModelAdmin):
    list_display = ("level", "prize", "received")
    list_filter = ("level", "prize")
    search_fields = ("level__title", "prize__title")
    ordering = ("-received",)
