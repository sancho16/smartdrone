from django.urls import path
from . import views
from . import api_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ── Web pages ──
    path('', views.home, name='home'),
    path('drones/', views.drone_list, name='drone_list'),
    path('drones/<int:pk>/', views.drone_detail, name='drone_detail'),
    path('drones/<int:pk>/buy/', views.buy_drone, name='buy_drone'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('repairs/', views.repair_home, name='repair_home'),
    path('repairs/request/', views.repair_request, name='repair_request'),
    path('repairs/track/<int:pk>/', views.repair_tracking, name='repair_tracking'),
    path('repairs/my/', views.my_repairs, name='my_repairs'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/repairs/', views.admin_repairs, name='admin_repairs'),
    path('set-lang/', views.set_lang, name='set_lang'),
    path('set-theme/', views.set_theme, name='set_theme'),

    # ── REST API ──
    path('api/drones/', api_views.DroneListAPI.as_view(), name='api_drones'),
    path('api/drones/<int:pk>/', api_views.DroneDetailAPI.as_view(), name='api_drone_detail'),
    path('api/drones/<int:drone_id>/order/', api_views.place_order, name='api_place_order'),
    path('api/orders/', api_views.MyOrdersAPI.as_view(), name='api_orders'),
    path('api/repairs/', api_views.RepairListCreateAPI.as_view(), name='api_repairs'),
    path('api/repairs/<int:pk>/', api_views.RepairDetailAPI.as_view(), name='api_repair_detail'),
    path('api/categories/', api_views.categories, name='api_categories'),
    path('api/auth/register/', api_views.register_api, name='api_register'),
    path('api/auth/me/', api_views.me, name='api_me'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='api_token'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]
