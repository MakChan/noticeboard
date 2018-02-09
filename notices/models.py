from django.db import models
from django.contrib.auth.models import User


class Notice(models.Model):
    title = models.TextField(max_length=60)
    message = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title