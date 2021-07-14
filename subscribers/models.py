from django.db import models

# Create your models here.


class Subscribers(models.Model):
    """Subscriber model"""

    email = models.CharField(blank=False, null=False,
                             help_text='Email address', max_length=100)
    full_name = models.CharField(
        max_length=100, blank=False, null=False, help_text='First & Last Name')

    def __str__(self):
        """Str representation of this object"""
        return self.full_name

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"
