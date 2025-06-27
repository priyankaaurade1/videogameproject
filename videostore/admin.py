from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(GameData)
class GameDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_id', 'staff', 'date', 'time', 'bill_no','photo')