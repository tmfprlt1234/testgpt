from django.contrib import admin

from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'amount', 'owner', 'created_at')
    search_fields = ('title', 'category', 'note', 'owner__username')
    list_filter = ('category', 'created_at')
