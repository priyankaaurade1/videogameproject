from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Store, GameData

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role and Store', {'fields': ('role', 'store')}),
    )
    list_display = ('username', 'role', 'store', 'is_active', 'is_staff')
    list_filter = ('role', 'store')

@admin.register(GameData)
class GameDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'machine_name', 'machine_number', 'get_store', 'staff', 'in_points', 'out_points', 'bill_no', 'date']
    list_filter = ['staff__store', 'date', 'expense_type']

    def get_store(self, obj):
        return obj.staff.store.name if obj.staff and obj.staff.store else "-"
    get_store.short_description = 'Store'
