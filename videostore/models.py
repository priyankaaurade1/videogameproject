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
    entry_source = models.CharField(
        max_length=30,
        choices=[('customer_staff_entry', 'Customer Entry')],
        default='customer_staff_entry'
    )

class ReadingData(models.Model):
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'staff'})
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    reading_no = models.CharField(max_length=100)
    reading_1 = models.PositiveIntegerField(default=0)
    reading_2 = models.PositiveIntegerField(default=0)
    reading_3 = models.PositiveIntegerField(default=0)
    reading_4 = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='uploads/', null=True, blank=True)
    entry_source = models.CharField(
        max_length=30,
        choices=[('staff_entry', 'Staff Entry')],
        default='staff_entry'
    )

class ReadingDataPhoto(models.Model):
    reading_data = models.ForeignKey(ReadingData, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='reading_photos/')

    def __str__(self):
        return f"Photo for {self.reading_data}"

