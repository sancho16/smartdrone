import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import torch

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from .models import Drone, Order, RepairRequest
from .utils import sync_drones_from_excel


def is_admin(user):
    return user.is_staff


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_chart(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return encoded


# ── Public views ─────────────────────────────────────────────────────────────

def home(request):
    drones = Drone.objects.filter(available=True)[:6]
    return render(request, 'shop/home.html', {'drones': drones})


def drone_list(request):
    category = request.GET.get('category', '')
    drones = Drone.objects.filter(available=True)
    if category:
        drones = drones.filter(category__icontains=category)
    categories = Drone.objects.values_list('category', flat=True).distinct()
    return render(request, 'shop/drone_list.html', {
        'drones': drones,
        'categories': categories,
        'selected_category': category,
    })


def drone_detail(request, pk):
    drone = get_object_or_404(Drone, pk=pk, available=True)
    return render(request, 'shop/drone_detail.html', {'drone': drone})


@login_required
def buy_drone(request, pk):
    drone = get_object_or_404(Drone, pk=pk, available=True)
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        if qty < 1 or qty > drone.stock:
            messages.error(request, 'Invalid quantity.')
            return redirect('drone_detail', pk=pk)
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
        messages.success(request, f'Order placed! Order #{order.id}')
        return redirect('my_orders')
    return redirect('drone_detail', pk=pk)


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/my_orders.html', {'orders': orders})


# ── Repair views ─────────────────────────────────────────────────────────────

def repair_home(request):
    return render(request, 'shop/repair_home.html')


def repair_request(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        device_type = request.POST.get('device_type', 'drone')
        brand_model = request.POST.get('brand_model', '').strip()
        issue_description = request.POST.get('issue_description', '').strip()
        urgency = request.POST.get('urgency', 'standard')

        if not full_name or not email or not brand_model or not issue_description:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'shop/repair_request.html', {'post': request.POST})

        repair = RepairRequest.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            device_type=device_type,
            brand_model=brand_model,
            issue_description=issue_description,
            urgency=urgency,
        )
        messages.success(request, f'Repair request #{repair.id} submitted! We will contact you at {email}.')
        return redirect('repair_tracking', pk=repair.id)

    return render(request, 'shop/repair_request.html', {})


def repair_tracking(request, pk):
    repair = get_object_or_404(RepairRequest, pk=pk)
    return render(request, 'shop/repair_tracking.html', {'repair': repair})


@login_required
def my_repairs(request):
    repairs = RepairRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/my_repairs.html', {'repairs': repairs})


# ── Auth views ───────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('home')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'shop/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        from django.contrib.auth.models import User
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'shop/register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'shop/register.html')
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f'Welcome, {username}!')
        return redirect('home')
    return render(request, 'shop/register.html')


# ── Admin dashboard ──────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Sync products from Excel on every dashboard load
    sync_drones_from_excel()

    total_drones = Drone.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(r=Sum('total_price'))['r'] or 0
    total_repairs = RepairRequest.objects.count()
    pending_repairs = RepairRequest.objects.filter(status='received').count()

    # ── Chart 1: Sales per drone (PyTorch tensor ops) ──
    orders_by_drone = (
        Order.objects.values('drone__name')
        .annotate(total=Sum('total_price'))
        .order_by('-total')[:8]
    )
    if orders_by_drone:
        labels = [o['drone__name'] for o in orders_by_drone]
        values = [float(o['total']) for o in orders_by_drone]
        t_values = torch.tensor(values, dtype=torch.float32)
        t_normalized = (t_values / t_values.sum() * 100).tolist()

        fig, ax = plt.subplots(figsize=(7, 4), facecolor='#0a0608')
        ax.set_facecolor('#110a0d')
        bars = ax.barh(labels, t_normalized, color='#7b1d2e', edgecolor='#c9a84c', linewidth=1.2)
        for bar, val in zip(bars, t_normalized):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    f'{val:.1f}%', va='center', color='#c9a84c', fontsize=9, fontweight='bold')
        ax.set_xlabel('Revenue Share (%)', color='#7a6068')
        ax.set_title('Sales Revenue by Drone', color='#c9a84c', fontsize=13, fontweight='bold')
        ax.tick_params(colors='#7a6068')
        for spine in ax.spines.values():
            spine.set_edgecolor('#221218')
        chart_sales = make_chart(fig)
    else:
        chart_sales = None

    # ── Chart 2: Orders over last 14 days ──
    today = timezone.now().date()
    days = [(today - timedelta(days=i)) for i in range(13, -1, -1)]
    counts = []
    for d in days:
        c = Order.objects.filter(created_at__date=d).count()
        counts.append(c)

    t_counts = torch.tensor(counts, dtype=torch.float32)
    smooth = torch.nn.functional.avg_pool1d(
        t_counts.unsqueeze(0).unsqueeze(0), kernel_size=3, stride=1, padding=1
    ).squeeze().tolist()

    fig2, ax2 = plt.subplots(figsize=(7, 4), facecolor='#0a0608')
    ax2.set_facecolor('#110a0d')
    ax2.fill_between(range(14), smooth, alpha=0.25, color='#9b2335')
    ax2.plot(range(14), smooth, color='#c9a84c', linewidth=2, marker='o', markersize=4, markerfacecolor='#7b1d2e')
    ax2.set_xticks(range(14))
    ax2.set_xticklabels([d.strftime('%m/%d') for d in days], rotation=45, color='#7a6068', fontsize=7)
    ax2.set_ylabel('Orders', color='#7a6068')
    ax2.set_title('Orders – Last 14 Days', color='#c9a84c', fontsize=13, fontweight='bold')
    ax2.tick_params(colors='#7a6068')
    for spine in ax2.spines.values():
        spine.set_edgecolor('#221218')
    chart_orders = make_chart(fig2)

    # ── Chart 3: Repair requests by device type ──
    repair_by_type = (
        RepairRequest.objects.values('device_type')
        .annotate(count=Count('id'))
    )
    if repair_by_type:
        r_labels = [r['device_type'].capitalize() for r in repair_by_type]
        r_values = [r['count'] for r in repair_by_type]
        t_r = torch.tensor(r_values, dtype=torch.float32)
        colors_pie = ['#7b1d2e', '#c9a84c', '#9b2335', '#8a6e2f']
        fig3, ax3 = plt.subplots(figsize=(5, 4), facecolor='#0a0608')
        ax3.set_facecolor('#0a0608')
        wedges, texts, autotexts = ax3.pie(
            t_r.tolist(), labels=r_labels, autopct='%1.0f%%',
            colors=colors_pie[:len(r_labels)], startangle=90,
            textprops={'color': '#f5ede8'}
        )
        for at in autotexts:
            at.set_color('#0a0608')
            at.set_fontweight('bold')
        ax3.set_title('Repairs by Device Type', color='#c9a84c', fontsize=13, fontweight='bold')
        chart_repairs_type = make_chart(fig3)
    else:
        chart_repairs_type = None

    # ── Chart 4: Repair status breakdown ──
    repair_by_status = (
        RepairRequest.objects.values('status')
        .annotate(count=Count('id'))
    )
    if repair_by_status:
        s_labels = [r['status'].replace('_', ' ').title() for r in repair_by_status]
        s_values = [r['count'] for r in repair_by_status]
        t_s = torch.tensor(s_values, dtype=torch.float32)
        fig4, ax4 = plt.subplots(figsize=(6, 4), facecolor='#0a0608')
        ax4.set_facecolor('#110a0d')
        bar_colors = ['#7b1d2e', '#c9a84c', '#9b2335', '#8a6e2f', '#c0394d', '#5a3030']
        ax4.bar(s_labels, t_s.tolist(), color=bar_colors[:len(s_labels)], edgecolor='#221218', linewidth=1.2)
        ax4.set_ylabel('Count', color='#7a6068')
        ax4.set_title('Repair Requests by Status', color='#c9a84c', fontsize=13, fontweight='bold')
        ax4.tick_params(colors='#7a6068', axis='both')
        plt.xticks(rotation=30, ha='right')
        for spine in ax4.spines.values():
            spine.set_edgecolor('#221218')
        chart_repairs_status = make_chart(fig4)
    else:
        chart_repairs_status = None

    recent_orders = Order.objects.order_by('-created_at')[:10]
    recent_repairs = RepairRequest.objects.order_by('-created_at')[:10]

    return render(request, 'shop/admin_dashboard.html', {
        'total_drones': total_drones,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_repairs': total_repairs,
        'pending_repairs': pending_repairs,
        'chart_sales': chart_sales,
        'chart_orders': chart_orders,
        'chart_repairs_type': chart_repairs_type,
        'chart_repairs_status': chart_repairs_status,
        'recent_orders': recent_orders,
        'recent_repairs': recent_repairs,
    })


@login_required
@user_passes_test(is_admin)
def admin_repairs(request):
    repairs = RepairRequest.objects.order_by('-created_at')
    if request.method == 'POST':
        repair_id = request.POST.get('repair_id')
        repair = get_object_or_404(RepairRequest, pk=repair_id)
        repair.status = request.POST.get('status', repair.status)
        repair.estimated_cost = request.POST.get('estimated_cost') or None
        repair.technician_notes = request.POST.get('technician_notes', '')
        repair.save()
        messages.success(request, f'Repair #{repair.id} updated.')
        return redirect('admin_repairs')
    return render(request, 'shop/admin_repairs.html', {'repairs': repairs})


# ── Language & Theme toggles ─────────────────────────────────────────────────

def set_lang(request):
    lang = request.GET.get('lang', 'es')
    if lang not in ('es', 'en'):
        lang = 'es'
    request.session['lang'] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))


def set_theme(request):
    theme = request.GET.get('theme', 'dark')
    if theme not in ('dark', 'light'):
        theme = 'dark'
    request.session['theme'] = theme
    return redirect(request.META.get('HTTP_REFERER', '/'))
