from django.db import models
from django.contrib.auth.models import User

class Todolist(models.Model):
    PRIORITY_CHOICES = (('low', "Low"),
                        ('medium', 'Medium'),
                        ('high','High'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False,null=True)
    created = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=200)

    def __str__(self):
        return self.item

