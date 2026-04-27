"""Run with: python seed_data.py"""
import os, sys, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from shop.models import Drone, Order, RepairRequest
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
import random

# ── Drones with real Unsplash/DJI-style images ──────────────────────────────
DRONES = [
    {
        'name': 'DJI Mini 4 Pro',
        'description': 'The lightest DJI drone under 249g with 4K/60fps HDR video, omnidirectional obstacle sensing, and 34-min flight time. Perfect for travel photography.',
        'price': Decimal('759.00'), 'stock': 12, 'category': 'Photography',
        'weight_kg': 0.249, 'flight_time_min': 34, 'range_km': 20,
        'image_url': 'https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=600&q=80',
    },
    {
        'name': 'DJI Air 3',
        'description': 'Dual main cameras with 1/1.3-inch CMOS sensors, 46-min max flight time, and omnidirectional obstacle sensing. The ultimate aerial photography drone.',
        'price': Decimal('1099.00'), 'stock': 7, 'category': 'Photography',
        'weight_kg': 0.720, 'flight_time_min': 46, 'range_km': 20,
        'image_url': 'https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=600&q=80',
    },
    {
        'name': 'DJI Mavic 3 Pro',
        'description': 'Triple-camera system with Hasselblad main camera, 43-min flight time, and 15km video transmission. Professional-grade aerial imaging.',
        'price': Decimal('2199.00'), 'stock': 4, 'category': 'Professional',
        'weight_kg': 0.958, 'flight_time_min': 43, 'range_km': 15,
        'image_url': 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=600&q=80',
    },
    {
        'name': 'DJI FPV Combo',
        'description': 'Immersive first-person view experience at up to 140 km/h. Emergency brake and hover, super-wide 150° FOV camera, and low-latency goggles included.',
        'price': Decimal('999.00'), 'stock': 5, 'category': 'FPV Racing',
        'weight_kg': 0.795, 'flight_time_min': 20, 'range_km': 10,
        'image_url': 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=600&q=80',
    },
    {
        'name': 'DJI Avata 2',
        'description': 'Next-gen FPV drone with 4K/60fps stabilized video, 23-min flight time, and redesigned propeller guards. Built for cinematic FPV flying.',
        'price': Decimal('1068.00'), 'stock': 6, 'category': 'FPV Racing',
        'weight_kg': 0.678, 'flight_time_min': 23, 'range_km': 13,
        'image_url': 'https://images.unsplash.com/photo-1601979031925-424e53b6caaa?w=600&q=80',
    },
    {
        'name': 'DJI Mini 3',
        'description': 'Lightweight under-249g drone with 4K video, 38-min flight time, and True Vertical Shooting for social media content. No registration required in most countries.',
        'price': Decimal('469.00'), 'stock': 18, 'category': 'Beginner',
        'weight_kg': 0.248, 'flight_time_min': 38, 'range_km': 12,
        'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=600&q=80',
    },
    {
        'name': 'Autel EVO Lite+',
        'description': '6K camera with a 1-inch CMOS sensor, 40-min flight time, and SkyLink 3.0 transmission up to 12km. A powerful DJI alternative.',
        'price': Decimal('849.00'), 'stock': 5, 'category': 'Photography',
        'weight_kg': 0.820, 'flight_time_min': 40, 'range_km': 12,
        'image_url': 'https://images.unsplash.com/photo-1534307671554-9a6d81f4d629?w=600&q=80',
    },
    {
        'name': 'Holy Stone HS720E',
        'description': 'GPS drone with 4K EIS camera, 23-min flight time, and follow-me mode. Great entry-level drone for beginners learning aerial photography.',
        'price': Decimal('199.00'), 'stock': 22, 'category': 'Beginner',
        'weight_kg': 0.500, 'flight_time_min': 23, 'range_km': 5,
        'image_url': 'https://images.unsplash.com/photo-1543872084-c7bd3822856f?w=600&q=80',
    },
    {
        'name': 'DJI Matrice 350 RTK',
        'description': 'Enterprise-grade drone with 55-min flight time, IP55 rating, and support for multiple payloads. Built for industrial inspection and mapping.',
        'price': Decimal('6999.00'), 'stock': 2, 'category': 'Enterprise',
        'weight_kg': 6.47, 'flight_time_min': 55, 'range_km': 20,
        'image_url': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=80',
    },
    {
        'name': 'DJI Neo',
        'description': 'Ultra-compact palm-sized drone at just 135g. AI subject tracking, 4K video, and one-tap social media modes. The most portable DJI ever.',
        'price': Decimal('199.00'), 'stock': 30, 'category': 'Beginner',
        'weight_kg': 0.135, 'flight_time_min': 18, 'range_km': 8,
        'image_url': 'https://images.unsplash.com/photo-1506947411487-a56738267384?w=600&q=80',
    },
]

print("Seeding drones...")
for d in DRONES:
    obj, created = Drone.objects.update_or_create(name=d['name'], defaults=d)
    print(f"  {'Created' if created else 'Updated'}: {obj.name}")

# ── Demo users ───────────────────────────────────────────────────────────────
print("\nSeeding users...")
demo_users = []
for uname, email in [('john_doe', 'john@example.com'), ('jane_smith', 'jane@example.com'), ('carlos_r', 'carlos@example.com')]:
    u, created = User.objects.get_or_create(username=uname, defaults={'email': email})
    if created:
        u.set_password('demo1234')
        u.save()
    demo_users.append(u)
    print(f"  {'Created' if created else 'Exists'}: {uname}")

# ── Demo orders ──────────────────────────────────────────────────────────────
print("\nSeeding orders...")
drones_list = list(Drone.objects.all())
statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'delivered', 'delivered']
for i in range(20):
    user = random.choice(demo_users)
    drone = random.choice(drones_list)
    qty = random.randint(1, 2)
    days_ago = random.randint(0, 30)
    o = Order.objects.create(
        user=user, drone=drone, quantity=qty,
        total_price=drone.price * qty,
        status=random.choice(statuses),
        created_at=timezone.now() - timedelta(days=days_ago),
    )
print(f"  Created 20 demo orders")

# ── Demo repair requests ─────────────────────────────────────────────────────
print("\nSeeding repair requests...")
REPAIRS = [
    ('Alice Johnson', 'alice@example.com', '555-0101', 'drone', 'DJI Mini 4 Pro', 'Crashed into a tree. Left front arm broken, motor not spinning.', 'express', 'in_repair', '120.00', 'Arm replaced, motor ordered. ETA 2 days.'),
    ('Bob Martinez', 'bob@example.com', '555-0102', 'camera', 'GoPro Hero 12', 'Lens cracked after water impact. Image blurry.', 'standard', 'diagnosing', None, 'Inspecting sensor for water damage.'),
    ('Carol White', 'carol@example.com', '555-0103', 'drone', 'DJI Mavic 3 Pro', 'Gimbal not stabilizing. Video shaky on all axes.', 'urgent', 'ready', '85.00', 'Gimbal ribbon replaced and calibrated. Ready for pickup.'),
    ('David Lee', 'david@example.com', '555-0104', 'drone', 'DJI FPV', 'ESC burnt out after crash. Drone powers on but motors dont spin.', 'standard', 'received', None, ''),
    ('Emma Davis', 'emma@example.com', '555-0105', 'camera', 'DJI Osmo Action 4', 'Screen cracked. Touch not working.', 'express', 'delivered', '65.00', 'Screen replaced. Tested and working.'),
    ('Frank Wilson', 'frank@example.com', '555-0106', 'drone', 'Autel EVO Lite+', 'GPS not locking. Drone drifts in position hold mode.', 'standard', 'in_repair', '95.00', 'GPS module replaced. Compass calibration in progress.'),
    ('Grace Kim', 'grace@example.com', '555-0107', 'drone', 'Holy Stone HS720E', 'Battery not charging. Charger light stays red.', 'standard', 'received', None, ''),
    ('Henry Brown', 'henry@example.com', '555-0108', 'camera', 'GoPro Hero 11', 'Overheating and shutting down during 4K recording.', 'express', 'diagnosing', None, 'Running thermal tests.'),
]
for r in REPAIRS:
    name, email, phone, dtype, model, issue, urgency, status, cost, notes = r
    days_ago = random.randint(0, 14)
    RepairRequest.objects.get_or_create(
        email=email, brand_model=model,
        defaults=dict(
            full_name=name, phone=phone, device_type=dtype,
            issue_description=issue, urgency=urgency, status=status,
            estimated_cost=cost, technician_notes=notes,
            created_at=timezone.now() - timedelta(days=days_ago),
        )
    )
    print(f"  Repair: {name} – {model}")

print("\n✅ Demo data seeded successfully!")
print("   Admin login: admin / admin123")
print("   Demo users:  john_doe / demo1234  |  jane_smith / demo1234")
