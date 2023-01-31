from django.db import models


# Create your models here.
class RepairContact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(verbose_name='email', max_length=255)
    contact_no = models.CharField(max_length=10)
    MY_CHOICES = (
        ('None', 'select option'),
        ('plumber', 'plumber'),
        ('electrician', 'electrician'),
        ('door repair', 'door repair')
    )
    type_of_repairs = models.CharField(max_length=100, choices=MY_CHOICES)




