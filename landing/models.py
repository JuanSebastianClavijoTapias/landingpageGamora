from django.db import models


class Lead(models.Model):
	name = models.CharField(max_length=120)
	company = models.CharField(max_length=120)
	email = models.EmailField()
	phone = models.CharField(max_length=40, blank=True)
	need = models.TextField(max_length=1200)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.name} - {self.company}'


class InteractionEvent(models.Model):
	channel = models.CharField(max_length=40)
	event_type = models.CharField(max_length=80)
	label = models.CharField(max_length=120, blank=True)
	target = models.URLField(max_length=500, blank=True)
	metadata = models.JSONField(default=dict, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.channel} - {self.event_type}'
