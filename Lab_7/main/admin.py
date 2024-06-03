from django.contrib import admin
from .models import Team, Player

class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1

class TeamAdmin(admin.ModelAdmin):
    inlines = [PlayerInline]

admin.site.register(Team, TeamAdmin)
admin.site.register(Player)
