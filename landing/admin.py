from django.contrib import admin

from .models import InteractionEvent, Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
	list_display = ('name', 'company', 'email', 'created_at')
	search_fields = ('name', 'company', 'email')
	list_filter = ('created_at',)


@admin.register(InteractionEvent)
class InteractionEventAdmin(admin.ModelAdmin):
	list_display = ('channel', 'event_type', 'label', 'created_at')
	search_fields = ('channel', 'event_type', 'label', 'target')
	list_filter = ('channel', 'event_type', 'created_at')

# Register your models here.
