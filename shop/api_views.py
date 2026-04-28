from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Drone, Order, RepairRequest
from .serializers import (
    DroneSerializer, OrderSerializer,
    RepairRequestSerializer, UserSerializer
)


# ── Drones ────────────────────────────────────────────────────────────────────

class DroneListAPI(generics.ListAPIView):
    serializer_class = DroneSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Drone.objects.filter(available=True)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__icontains=category)
        return qs


class DroneDetailAPI(generics.RetrieveAPIView):
    queryset = Drone.objects.filter(available=True)
    serializer_class = DroneSerializer
    permission_classes = [AllowAny]


# ── Orders ────────────────────────────────────────────────────────────────────

class MyOrdersAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request, drone_id):
    try:
        drone = Drone.objects.get(pk=drone_id, available=True)
    except Drone.DoesNotExist:
        return Response({'error': 'Drone not found'}, status=404)

    qty = int(request.data.get('quantity', 1))
    if qty < 1 or qty > drone.stock:
        return Response({'error': 'Invalid quantity'}, status=400)

    order = Order.objects.create(
        user=request.user,
        drone=drone,
        quantity=qty,
        total_price=drone.price * qty,
    )
    drone.stock -= qty
    if drone.stock == 0:
        drone.available = False
    drone.save()
    return Response(OrderSerializer(order).data, status=201)


# ── Repairs ───────────────────────────────────────────────────────────────────

class RepairListCreateAPI(generics.ListCreateAPIView):
    serializer_class = RepairRequestSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return RepairRequest.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


class RepairDetailAPI(generics.RetrieveAPIView):
    queryset = RepairRequest.objects.all()
    serializer_class = RepairRequestSerializer
    permission_classes = [AllowAny]


# ── Auth ──────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    username = request.data.get('username', '').strip()
    email = request.data.get('email', '').strip()
    password = request.data.get('password', '')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response(UserSerializer(user).data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


# ── Categories ────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def categories(request):
    cats = Drone.objects.values_list('category', flat=True).distinct()
    return Response([c for c in cats if c])
