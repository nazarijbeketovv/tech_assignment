from django.contrib import admin

from apps.task_1.models.player import Boost, Player



@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("user", "points", "first_login", "last_login")
    search_fields = ("user__username", "points")
    list_filter = ("first_login", "last_login")
    ordering = ("-points", "-last_login")


@admin.register(Boost)
class BoostAdmin(admin.ModelAdmin):
    list_display = ("player", "boost_type", "duration", "activated_at", "is_active")
    search_fields = ("player__user__username", "boost_type")
    list_filter = ("boost_type", "is_active")
    ordering = ("-activated_at", "duration")
    readonly_fields = ("activated_at",)
