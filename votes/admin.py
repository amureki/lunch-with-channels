from django.contrib import admin

from .models import Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ('username', 'place', 'created')
    readonly_fields = ('created',)


admin.site.register(Vote, VoteAdmin)
