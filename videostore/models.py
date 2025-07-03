from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'SuperAdmin'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True)

class Machine(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.number})"

class GameData(models.Model):
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'staff'})
    customer_id = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=100)
    in_points = models.PositiveIntegerField()
    out_points = models.PositiveIntegerField()
    good_luck = models.PositiveIntegerField()
    expense_type = models.CharField(max_length=50, 
        choices = [
            ('salary', 'Salary'),
            ('tea', 'Tea'),
            ('water', 'Water'),
            ('lightbill', 'Light Bill'),
            ('police', 'Police'),
            ('goodluck', 'Good Luck'),
            ('other', 'Other'),
    ])
    expense_amt = models.PositiveIntegerField(default=0)
    bill_no = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='uploads/', null=True, blank=True)
    remarks = models.TextField(blank=True)
