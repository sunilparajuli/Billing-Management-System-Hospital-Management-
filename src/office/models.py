from django.db import models

# Create your models here.
class Office(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    pan = models.CharField(max_length=200, blank=True, null=True)
    vat = models.CharField(max_length=200, blank=True, null=True)
    created_at =   models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' %(self.name)   