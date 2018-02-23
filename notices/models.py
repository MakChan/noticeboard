from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from markdown import markdown


class Notice(models.Model):
	title = models.CharField(max_length=100)
	message = models.TextField(max_length=2000)
	created_at = models.DateTimeField(auto_now_add=True)
	tags = models.CharField(max_length=100, null=True)
	created_by = models.ForeignKey(User, related_name='posts', on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.title

	def get_message_as_markdown(self):
		return mark_safe(markdown(self.message, safe_mode='escape'))       

	def get_tags_as_list(self):
		return self.tags.split(",")[:-1]