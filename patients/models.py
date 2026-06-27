from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.validators import phone_validator


class Patient(models.Model):
    """
    A patient record owned by the authenticated user who created it.
    Patients are private: a user can only see, update, or delete the
    patients they personally added (enforced in patients/views.py
    and core/permissions.py).
    """

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField(blank=True, default='')
    phone_number = models.CharField(max_length=16, validators=[phone_validator], blank=True, default='')
    medical_history = models.TextField(
        blank=True, default='', help_text='Optional free-text notes (allergies, conditions, etc.)'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patients',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} (added by user #{self.created_by_id})'
