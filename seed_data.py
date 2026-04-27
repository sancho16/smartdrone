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

DRONES = [
    {
        'name': 'DJI Mini 4 Pro',
        'description': 'El dron más avanzado bajo 249g. Vídeo 4K/60fps HDR, detección omnidireccional, ActiveTrack 360° y 34 min de vuelo.',
        'price': Decimal('759.00'), 'stock': 12, 'category': 'Fotografía',
        'weight_kg': 0.249, 'flight_time_min': 34, 'range_km': 20,
        'image_url': 'https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Air 3',
        'description': 'Doble cámara CMOS 1/1.3", 46 min de vuelo, detección omnidireccional y transmisión O4 hasta 20 km.',
        'price': Decimal('1099.00'), 'stock': 7, 'category': 'Fotografía',
        'weight_kg': 0.720, 'flight_time_min': 46, 'range_km': 20,
        'image_url': 'https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Mavic 3 Pro',
        'description': 'Triple cámara con cámara principal Hasselblad, 43 min de vuelo y transmisión a 15 km. Imagen aérea profesional.',
        'price': Decimal('2199.00'), 'stock': 4, 'category': 'Profesional',
        'weight_kg': 0.958, 'flight_time_min': 43, 'range_km': 15,
        'image_url': 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Mavic 3 Classic',
        'description': 'Cámara Hasselblad sensor 4/3 CMOS, apertura f/2.8–f/11, 46 min de vuelo. La elección del fotógrafo serio.',
        'price': Decimal('1499.00'), 'stock': 6, 'category': 'Profesional',
        'weight_kg': 0.895, 'flight_time_min': 46, 'range_km': 15,
        'image_url': 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI FPV Combo',
        'description': 'Experiencia FPV inmersiva a 140 km/h. Freno de emergencia, cámara 150° FOV y gafas de baja latencia incluidas.',
        'price': Decimal('999.00'), 'stock': 5, 'category': 'FPV Racing',
        'weight_kg': 0.795, 'flight_time_min': 20, 'range_km': 10,
        'image_url': 'https://images.unsplash.com/photo-1601979031925-424e53b6caaa?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Avata 2',
        'description': 'FPV de nueva generación con vídeo 4K/60fps estabilizado, 23 min de vuelo y guardas de hélice rediseñadas.',
        'price': Decimal('1068.00'), 'stock': 6, 'category': 'FPV Racing',
        'weight_kg': 0.678, 'flight_time_min': 23, 'range_km': 13,
        'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Mini 3 Pro',
        'description': 'Bajo 249g con detección en 3 direcciones, 4K/60fps, Tiro Vertical Verdadero y 34 min de vuelo.',
        'price': Decimal('759.00'), 'stock': 10, 'category': 'Fotografía',
        'weight_kg': 0.249, 'flight_time_min': 34, 'range_km': 12,
        'image_url': 'https://images.unsplash.com/photo-1534307671554-9a6d81f4d629?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Mini 3',
        'description': 'Bajo 249g con vídeo 4K, 38 min de vuelo y Tiro Vertical Verdadero para redes sociales.',
        'price': Decimal('469.00'), 'stock': 18, 'category': 'Principiante',
        'weight_kg': 0.248, 'flight_time_min': 38, 'range_km': 12,
        'image_url': 'https://images.unsplash.com/photo-1543872084-c7bd3822856f?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Neo',
        'description': 'Ultracompacto 135g. Seguimiento IA, vídeo 4K y modos de redes sociales con un toque. El DJI más portátil.',
        'price': Decimal('199.00'), 'stock': 30, 'category': 'Principiante',
        'weight_kg': 0.135, 'flight_time_min': 18, 'range_km': 8,
        'image_url': 'https://images.unsplash.com/photo-1506947411487-a56738267384?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Air 2S',
        'description': 'Sensor CMOS 1 pulgada, vídeo 5.4K, detección en 5 direcciones y 31 min de vuelo. Potencia profesional compacta.',
        'price': Decimal('799.00'), 'stock': 9, 'category': 'Fotografía',
        'weight_kg': 0.595, 'flight_time_min': 31, 'range_km': 12,
        'image_url': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Matrice 350 RTK',
        'description': 'Dron empresarial con 55 min de vuelo, IP55 y soporte múltiples cargas. Para inspección industrial y cartografía.',
        'price': Decimal('6999.00'), 'stock': 2, 'category': 'Empresarial',
        'weight_kg': 6.47, 'flight_time_min': 55, 'range_km': 20,
        'image_url': 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Inspire 3',
        'description': 'Dron cinematográfico con cámara Zenmuse X9-8K, 28 min de vuelo y sistema de doble operador. Estándar de la industria.',
        'price': Decimal('16499.00'), 'stock': 1, 'category': 'Cine',
        'weight_kg': 9.7, 'flight_time_min': 28, 'range_km': 15,
        'image_url': 'https://images.unsplash.com/photo-1527786356703-4b100091cd2c?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Mavic 3 Enterprise',
        'description': 'Cámara térmica opcional, RTK integrado y 45 min de vuelo. Para inspección, búsqueda y rescate.',
        'price': Decimal('3499.00'), 'stock': 3, 'category': 'Empresarial',
        'weight_kg': 0.915, 'flight_time_min': 45, 'range_km': 15,
        'image_url': 'https://images.unsplash.com/photo-1561484930-998b6a7b22e8?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Avata',
        'description': 'Primer FPV DJI con guardas integradas. Vídeo 4K, 18 min de vuelo y control intuitivo con movimientos del cuerpo.',
        'price': Decimal('629.00'), 'stock': 8, 'category': 'FPV Racing',
        'weight_kg': 0.410, 'flight_time_min': 18, 'range_km': 10,
        'image_url': 'https://images.unsplash.com/photo-1592659762303-90081d34b277?w=800&q=90&fit=crop',
    },
    {
        'name': 'Autel EVO Nano+',
        'description': 'Ultraligero 249g con sensor 1/1.28", apertura f/1.9 y 28 min de vuelo. Calidad premium en formato mini.',
        'price': Decimal('649.00'), 'stock': 7, 'category': 'Fotografía',
        'weight_kg': 0.249, 'flight_time_min': 28, 'range_km': 10,
        'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=90&fit=crop',
    },
    {
        'name': 'Autel EVO Lite+',
        'description': 'Cámara 6K sensor 1 pulgada, 40 min de vuelo y transmisión SkyLink 3.0 hasta 12 km.',
        'price': Decimal('849.00'), 'stock': 5, 'category': 'Fotografía',
        'weight_kg': 0.820, 'flight_time_min': 40, 'range_km': 12,
        'image_url': 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=800&q=90&fit=crop',
    },
    {
        'name': 'Holy Stone HS720E',
        'description': 'GPS con cámara 4K EIS, 23 min de vuelo y follow-me. Ideal para principiantes en fotografía aérea.',
        'price': Decimal('199.00'), 'stock': 22, 'category': 'Principiante',
        'weight_kg': 0.500, 'flight_time_min': 23, 'range_km': 5,
        'image_url': 'https://images.unsplash.com/photo-1543872084-c7bd3822856f?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Phantom 4 RTK',
        'description': 'Dron de mapeo con RTK integrado, precisión centimétrica y 30 min de vuelo. El estándar para topografía y agrimensura.',
        'price': Decimal('5799.00'), 'stock': 3, 'category': 'Empresarial',
        'weight_kg': 1.391, 'flight_time_min': 30, 'range_km': 7,
        'image_url': 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=800&q=90&fit=crop',
    },
    {
        'name': 'DJI Mini 2 SE',
        'description': 'El dron más accesible de DJI. Vídeo 2.7K, 31 min de vuelo y transmisión hasta 10 km. Perfecto para empezar.',
        'price': Decimal('299.00'), 'stock': 25, 'category': 'Principiante',
        'weight_kg': 0.246, 'flight_time_min': 31, 'range_km': 10,
        'image_url': 'https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=800&q=90&fit=crop',
    },
    {
        'name': 'Skydio 2+',
        'description': 'El dron de seguimiento autónomo más avanzado. 6 cámaras de navegación, evitación de obstáculos 360° y seguimiento deportivo.',
        'price': Decimal('1099.00'), 'stock': 4, 'category': 'Fotografía',
        'weight_kg': 0.800, 'flight_time_min': 27, 'range_km': 6,
        'image_url': 'https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=800&q=90&fit=crop',
    },
]

print("Seeding drones...")
Drone.objects.all().delete()
for d in DRONES:
    obj = Drone.objects.create(**d)
    print(f"  Created: {obj.name}")

# ── Demo users ────────────────────────────────────────────────────────────────
print("\nSeeding users...")
demo_users = []
for uname, email in [('john_doe', 'john@example.com'), ('jane_smith', 'jane@example.com'), ('carlos_r', 'carlos@example.com')]:
    u, created = User.objects.get_or_create(username=uname, defaults={'email': email})
    if created:
        u.set_password('demo1234')
        u.save()
    demo_users.append(u)
    print(f"  {'Created' if created else 'Exists'}: {uname}")

# ── Demo orders ───────────────────────────────────────────────────────────────
print("\nSeeding orders...")
Order.objects.all().delete()
drones_list = list(Drone.objects.all())
statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'delivered', 'delivered']
for i in range(30):
    user = random.choice(demo_users)
    drone = random.choice(drones_list)
    qty = random.randint(1, 2)
    days_ago = random.randint(0, 30)
    Order.objects.create(
        user=user, drone=drone, quantity=qty,
        total_price=drone.price * qty,
        status=random.choice(statuses),
        created_at=timezone.now() - timedelta(days=days_ago),
    )
print("  Created 30 demo orders")

# ── Demo repairs ──────────────────────────────────────────────────────────────
print("\nSeeding repair requests...")
RepairRequest.objects.all().delete()
REPAIRS = [
    ('Alice Johnson',  'alice@example.com',  '555-0101', 'drone',  'DJI Mini 4 Pro',     'Brazo delantero roto tras colisión. Motor no gira.',                    'express',  'in_repair',  '120.00', 'Brazo reemplazado, motor en camino. ETA 2 días.'),
    ('Bob Martínez',   'bob@example.com',    '555-0102', 'camera', 'GoPro Hero 12',       'Lente rota tras impacto con agua. Imagen borrosa.',                    'standard', 'diagnosing', None,     'Inspeccionando sensor por daño de agua.'),
    ('Carol White',    'carol@example.com',  '555-0103', 'drone',  'DJI Mavic 3 Pro',     'Gimbal no estabiliza. Vídeo tembloroso en todos los ejes.',            'urgent',   'ready',      '85.00',  'Cinta del gimbal reemplazada y calibrada. Listo para recoger.'),
    ('David Lee',      'david@example.com',  '555-0104', 'drone',  'DJI FPV',             'ESC quemado tras accidente. Enciende pero motores no giran.',          'standard', 'received',   None,     ''),
    ('Emma Davis',     'emma@example.com',   '555-0105', 'camera', 'DJI Osmo Action 4',   'Pantalla rota. Táctil no responde.',                                   'express',  'delivered',  '65.00',  'Pantalla reemplazada. Probado y funcionando.'),
    ('Frank Wilson',   'frank@example.com',  '555-0106', 'drone',  'Autel EVO Lite+',     'GPS no conecta. Dron deriva en modo de posición.',                    'standard', 'in_repair',  '95.00',  'Módulo GPS reemplazado. Calibración de brújula en progreso.'),
    ('Grace Kim',      'grace@example.com',  '555-0107', 'drone',  'Holy Stone HS720E',   'Batería no carga. Luz del cargador permanece roja.',                   'standard', 'received',   None,     ''),
    ('Henry Brown',    'henry@example.com',  '555-0108', 'camera', 'GoPro Hero 11',       'Se sobrecalienta y apaga durante grabación 4K.',                      'express',  'diagnosing', None,     'Realizando pruebas térmicas.'),
    ('Laura Gómez',    'laura@example.com',  '555-0109', 'drone',  'DJI Air 3',           'Hélice rota y motor vibrando. Necesita revisión completa.',            'express',  'in_repair',  '75.00',  'Hélices reemplazadas. Revisando balanceo de motores.'),
    ('Miguel Torres',  'miguel@example.com', '555-0110', 'camera', 'DJI Osmo Pocket 3',   'Gimbal bloqueado. No se mueve en ningún eje.',                        'urgent',   'ready',      '110.00', 'Motor del gimbal reemplazado. Calibrado y listo.'),
]
for r in REPAIRS:
    name, email, phone, dtype, model, issue, urgency, status, cost, notes = r
    days_ago = random.randint(0, 14)
    RepairRequest.objects.create(
        full_name=name, email=email, phone=phone, device_type=dtype,
        brand_model=model, issue_description=issue, urgency=urgency,
        status=status, estimated_cost=cost, technician_notes=notes,
        created_at=timezone.now() - timedelta(days=days_ago),
    )
    print(f"  Repair: {name} – {model}")

print("\n✅ Datos de demo cargados exitosamente!")
print("   Admin: admin / admin123")
print("   Usuarios demo: john_doe / demo1234  |  jane_smith / demo1234")
