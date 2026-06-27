from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.validators import phone_validator


class Doctor(models.Model):
    """
    A doctor record. Unlike Patient, doctors form a shared directory:
    every authenticated user can list and view all doctors (GET is
    open), but only the user who added a given doctor may update or
    delete it (enforced by IsOwnerForWriteElseAuthenticated).
    """

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)], null=True, blank=True
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    phone_number = models.CharField(max_length=16, validators=[phone_validator], blank=True, default='')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctors',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Dr. {self.name} ({self.specialization})'
