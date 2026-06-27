from django.core.validators import RegexValidator

# Shared across the Patient and Doctor models so both apps validate
# phone numbers the same way without depending on each other.
phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message='Enter a valid phone number (7-15 digits, optionally starting with +).',
)
