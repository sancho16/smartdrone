from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('drones/', views.drone_list, name='drone_list'),
    path('drones/<int:pk>/', views.drone_detail, name='drone_detail'),
    path('drones/<int:pk>/buy/', views.buy_drone, name='buy_drone'),
    path('my-orders/', views.my_orders, name='my_orders'),

    # Repairs
    path('repairs/', views.repair_home, name='repair_home'),
    path('repairs/request/', views.repair_request, name='repair_request'),
    path('repairs/track/<int:pk>/', views.repair_tracking, name='repair_tracking'),
    path('repairs/my/', views.my_repairs, name='my_repairs'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # UI toggles
    path('set-lang/', views.set_lang, name='set_lang'),
    path('set-theme/', views.set_theme, name='set_theme'),

    # Admin
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/repairs/', views.admin_repairs, name='admin_repairs'),
]
