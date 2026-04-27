from django.contrib import admin
from .models import Drone, Order, RepairRequest

@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'category']
    list_filter = ['available', 'category']
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'drone', 'quantity', 'total_price', 'status', 'created_at']
    list_filter = ['status']

@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'device_type', 'brand_model', 'urgency', 'status', 'estimated_cost', 'created_at']
    list_filter = ['status', 'device_type', 'urgency']
    search_fields = ['full_name', 'email', 'brand_model']
    readonly_fields = ['created_at', 'updated_at']
