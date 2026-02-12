from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('facilities', 'Facilities'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    temperature = models.FloatField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='classrooms'
    )

    def status(self):
        if self.temperature < 20:
            return "cold"
        elif 20 <= self.temperature <= 26:
            return "optimal"
        return "hot"

    def __str__(self):
        return self.name
