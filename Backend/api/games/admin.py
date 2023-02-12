from django.contrib import admin

from games.models import GamesModel


class GamesAdmin(admin.ModelAdmin):
    pass


admin.site.register(GamesModel, GamesAdmin)
