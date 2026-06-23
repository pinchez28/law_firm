from django.db import models


class LawFirm(models.Model):
    name = models.CharField(max_length=255)

    registration_number = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)

    address = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name