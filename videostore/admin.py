from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role and Store', {'fields': ('role', 'store')}),
    )
    list_display = ('username', 'role', 'store','phone_number', 'is_active', 'is_staff')
    list_filter = ('role', 'store')

@admin.register(ReadingData)
class ReadingDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff', 'machine', 'reading_no', 'date', 'time']

