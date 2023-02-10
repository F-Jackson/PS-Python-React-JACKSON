from django.contrib import admin
from .models import *


class RefreshTokensAdmin(admin.ModelAdmin):
    pass


admin.site.register(RefreshTokens, RefreshTokensAdmin)
