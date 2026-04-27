from django.db import models
from django.contrib.auth.models import User


class Drone(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='drones/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='External image URL (used if no uploaded image)')
    category = models.CharField(max_length=100, blank=True)
    weight_kg = models.FloatField(default=0)
    flight_time_min = models.IntegerField(default=0)
    range_km = models.FloatField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.drone.name}"


class RepairRequest(models.Model):
    DEVICE_CHOICES = [
        ('drone', 'Drone'),
        ('camera', 'Camera'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('diagnosing', 'Diagnosing'),
        ('in_repair', 'In Repair'),
        ('ready', 'Ready for Pickup'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    URGENCY_CHOICES = [
        ('standard', 'Standard (5-7 days)'),
        ('express', 'Express (2-3 days)'),
        ('urgent', 'Urgent (24h)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_CHOICES, default='drone')
    brand_model = models.CharField(max_length=200, verbose_name='Brand / Model')
    issue_description = models.TextField()
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='standard')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    estimated_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    technician_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Repair #{self.id} – {self.full_name} – {self.brand_model}"

    class Meta:
        ordering = ['-created_at']
