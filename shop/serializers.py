from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Drone, Order, RepairRequest


class DroneSerializer(serializers.ModelSerializer):
    image_src = serializers.SerializerMethodField()

    class Meta:
        model = Drone
        fields = [
            'id', 'name', 'description', 'price', 'stock',
            'category', 'weight_kg', 'flight_time_min', 'range_km',
            'available', 'image_url', 'image_src',
        ]

    def get_image_src(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return obj.image_url or None


class OrderSerializer(serializers.ModelSerializer):
    drone_name = serializers.CharField(source='drone.name', read_only=True)
    drone_image = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'drone', 'drone_name', 'drone_image',
                  'quantity', 'total_price', 'status', 'created_at']
        read_only_fields = ['total_price', 'status', 'created_at']

    def get_drone_image(self, obj):
        return obj.drone.image_url or None


class RepairRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRequest
        fields = [
            'id', 'full_name', 'email', 'phone', 'device_type',
            'brand_model', 'issue_description', 'urgency',
            'status', 'estimated_cost', 'technician_notes', 'created_at',
        ]
        read_only_fields = ['status', 'estimated_cost', 'technician_notes', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
