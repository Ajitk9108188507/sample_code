from django.db import models
from django.db import models


class Task(models.Model):

    PRIORITY_CHOICES = [("LOW", "Low"),("MEDIUM", "Medium"),("HIGH", "High"),]

    STATUS_CHOICES = [("PENDING", "Pending"),("COMPLETED", "Completed"),("LOCKED", "Locked"),("EXPIRED", "Expired"),]

    title = models.CharField(max_length=200)

    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES)

    estimated_time = models.PositiveIntegerField(help_text="Estimated time in minutes")

    created_at = models.DateTimeField( auto_now_add=True)

    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default="PENDING")

    locked_until = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.title