from django import template

register = template.Library()

TRANSLATIONS = {
    # Navbar
    'nav_shop':        {'es': 'Tienda',        'en': 'Shop'},
    'nav_repairs':     {'es': 'Reparaciones',  'en': 'Repairs'},
    'nav_orders':      {'es': 'Pedidos',       'en': 'Orders'},
    'nav_my_repairs':  {'es': 'Mis Reparaciones', 'en': 'My Repairs'},
    'nav_dashboard':   {'es': 'Panel Admin',   'en': 'Dashboard'},
    'nav_login':       {'es': 'Iniciar Sesión','en': 'Login'},
    'nav_register':    {'es': 'Registrarse',   'en': 'Register'},
    'nav_logout':      {'es': 'Cerrar Sesión', 'en': 'Logout'},

    # Home hero
    'hero_badge':      {'es': 'Tecnología Drone Premium', 'en': 'Premium Drone Technology'},
    'hero_h1a':        {'es': 'Vuela Más Lejos.', 'en': 'Fly Further.'},
    'hero_h1b':        {'es': 'Repara Más Inteligente.', 'en': 'Repair Smarter.'},
    'hero_sub':        {'es': 'Drones premium en venta y servicios profesionales de reparación para drones y cámaras. Rápido, confiable, experto.', 'en': 'Premium drones for sale and professional repair services for drones & cameras. Fast, reliable, expert.'},
    'hero_btn_shop':   {'es': 'Ver Drones',    'en': 'Shop Drones'},
    'hero_btn_repair': {'es': 'Servicio de Reparación', 'en': 'Repair Service'},
    'chip_models':     {'es': '50+ Modelos',   'en': '50+ Models'},
    'chip_techs':      {'es': 'Técnicos Expertos', 'en': 'Expert Technicians'},
    'chip_urgent':     {'es': 'Reparación Urgente 24h', 'en': '24h Urgent Repair'},

    # Services
    'svc_sales_title': {'es': 'Venta de Drones', 'en': 'Drone Sales'},
    'svc_sales_desc':  {'es': 'Drones DJI, Autel y FPV de primera línea para fotografía, carreras y uso comercial.', 'en': 'Top-of-the-line DJI, Autel and FPV drones for photography, racing, and commercial use.'},
    'svc_sales_btn':   {'es': 'Ver Drones',    'en': 'Browse Drones'},
    'svc_drone_title': {'es': 'Reparación de Drones', 'en': 'Drone Repairs'},
    'svc_drone_desc':  {'es': 'Motores, ESC, chasis, controladores de vuelo, GPS — reparamos todas las marcas con garantía.', 'en': 'Motors, ESCs, frames, flight controllers, GPS — we fix all major brands with a warranty.'},
    'svc_drone_btn':   {'es': 'Solicitar Reparación', 'en': 'Request Repair'},
    'svc_cam_title':   {'es': 'Reparación de Cámaras', 'en': 'Camera Repairs'},
    'svc_cam_desc':    {'es': 'Reparación de gimbal, lente, sensor y cámara FPV. Especialistas en GoPro, DJI Osmo y cámaras de acción.', 'en': 'Gimbal, lens, sensor and FPV camera repairs. GoPro, DJI Osmo, and action cam specialists.'},
    'svc_cam_btn':     {'es': 'Solicitar Reparación', 'en': 'Request Repair'},

    # Featured
    'featured_title':  {'es': '✦ Drones Destacados', 'en': '✦ Featured Drones'},
    'view_all':        {'es': 'Ver Todos',     'en': 'View All'},
    'view_details':    {'es': 'Ver Detalles',  'en': 'View Details'},

    # Drone list
    'drones_title':    {'es': 'Drones en Venta', 'en': 'Drones for Sale'},
    'all_filter':      {'es': 'Todos',         'en': 'All'},
    'in_stock':        {'es': 'en stock',      'en': 'in stock'},
    'no_drones':       {'es': 'No hay drones disponibles por ahora.', 'en': 'No drones available right now.'},

    # Drone detail
    'back_drones':     {'es': '← Volver a Drones', 'en': '← Back to Drones'},
    'in_stock_badge':  {'es': 'En Stock',      'en': 'In Stock'},
    'out_of_stock':    {'es': 'Sin Stock',     'en': 'Out of Stock'},
    'flight_time':     {'es': 'Vuelo',         'en': 'Flight Time'},
    'range_lbl':       {'es': 'Alcance',       'en': 'Range'},
    'weight_lbl':      {'es': 'Peso',          'en': 'Weight'},
    'stock_lbl':       {'es': 'Stock',         'en': 'Stock'},
    'buy_now':         {'es': 'Comprar Ahora', 'en': 'Buy Now'},
    'login_to_buy':    {'es': 'Inicia Sesión para Comprar', 'en': 'Login to Buy'},
    'need_repair':     {'es': '¿Necesitas una reparación?', 'en': 'Need a repair instead?'},

    # My orders
    'my_orders_title': {'es': 'Mis Pedidos',   'en': 'My Orders'},
    'col_drone':       {'es': 'Drone',         'en': 'Drone'},
    'col_qty':         {'es': 'Cant.',         'en': 'Qty'},
    'col_total':       {'es': 'Total',         'en': 'Total'},
    'col_status':      {'es': 'Estado',        'en': 'Status'},
    'col_date':        {'es': 'Fecha',         'en': 'Date'},
    'no_orders':       {'es': 'Aún no tienes pedidos.', 'en': 'No orders yet.'},
    'shop_drones_btn': {'es': 'Ver Drones',    'en': 'Shop Drones'},

    # Repair home
    'repair_title':    {'es': 'Servicios de Reparación', 'en': 'Repair Services'},
    'repair_sub':      {'es': 'Reparación profesional de drones y cámaras — rápida, confiable y asequible', 'en': 'Professional drone & camera repair — fast, reliable, affordable'},
    'repair_cta':      {'es': 'Enviar Solicitud de Reparación', 'en': 'Submit a Repair Request'},
    'what_we_repair':  {'es': 'Qué Reparamos', 'en': 'What We Repair'},
    'turnaround':      {'es': 'Tiempos de Entrega', 'en': 'Turnaround Times'},
    'standard_lbl':    {'es': 'Estándar',      'en': 'Standard'},
    'express_lbl':     {'es': 'Express',       'en': 'Express'},
    'urgent_lbl':      {'es': 'Urgente',       'en': 'Urgent'},
    'std_days':        {'es': '5–7 días hábiles', 'en': '5–7 business days'},
    'exp_days':        {'es': '2–3 días hábiles', 'en': '2–3 business days'},
    'urg_days':        {'es': 'En 24 horas',   'en': 'Within 24 hours'},
    'most_affordable': {'es': 'Más económico', 'en': 'Most affordable'},
    'faster_turn':     {'es': 'Más rápido',    'en': 'Faster turnaround'},
    'priority_svc':    {'es': 'Servicio prioritario', 'en': 'Priority service'},
    'start_repair_btn':{'es': 'Iniciar Solicitud de Reparación', 'en': 'Start Your Repair Request'},

    # Repair request form
    'repair_req_title':{'es': 'Solicitud de Reparación', 'en': 'Repair Request'},
    'repair_req_sub':  {'es': 'Completa el formulario y te contactaremos con un presupuesto en 24h.', 'en': 'Fill in the form and we\'ll get back to you with a quote within 24h.'},
    'your_details':    {'es': 'Tus Datos',     'en': 'Your Details'},
    'full_name_lbl':   {'es': 'Nombre Completo', 'en': 'Full Name'},
    'email_lbl':       {'es': 'Correo Electrónico', 'en': 'Email'},
    'phone_lbl':       {'es': 'Teléfono',      'en': 'Phone'},
    'device_info':     {'es': 'Información del Dispositivo', 'en': 'Device Information'},
    'device_type_lbl': {'es': 'Tipo de Dispositivo', 'en': 'Device Type'},
    'brand_model_lbl': {'es': 'Marca / Modelo','en': 'Brand / Model'},
    'issue_lbl':       {'es': 'Describe el Problema', 'en': 'Describe the Issue'},
    'issue_ph':        {'es': '¿Qué pasó? ¿Qué síntomas observas?', 'en': 'What happened? What symptoms are you seeing?'},
    'service_speed':   {'es': 'Velocidad del Servicio', 'en': 'Service Speed'},
    'submit_repair':   {'es': 'Enviar Solicitud', 'en': 'Submit Repair Request'},
    'opt_drone':       {'es': 'Drone',         'en': 'Drone'},
    'opt_camera':      {'es': 'Cámara',        'en': 'Camera'},
    'opt_other':       {'es': 'Otro',          'en': 'Other'},

    # Repair tracking
    'repair_track_title': {'es': 'Reparación', 'en': 'Repair'},
    'submitted_lbl':   {'es': 'Enviado',       'en': 'Submitted'},
    'customer_lbl':    {'es': 'Cliente',       'en': 'Customer'},
    'device_lbl':      {'es': 'Dispositivo',   'en': 'Device'},
    'urgency_lbl':     {'es': 'Urgencia',      'en': 'Urgency'},
    'est_cost_lbl':    {'es': 'Costo Estimado','en': 'Estimated Cost'},
    'issue_desc_lbl':  {'es': 'Descripción del Problema', 'en': 'Issue Description'},
    'tech_notes_lbl':  {'es': 'Notas del Técnico', 'en': 'Technician Notes'},
    'back_repairs':    {'es': '← Volver a Reparaciones', 'en': '← Back to Repairs'},
    'my_repairs_btn':  {'es': 'Mis Reparaciones', 'en': 'My Repairs'},

    # My repairs
    'my_repairs_title':{'es': 'Mis Solicitudes de Reparación', 'en': 'My Repair Requests'},
    'track_repair_btn':{'es': 'Rastrear Reparación', 'en': 'Track Repair'},
    'no_repairs':      {'es': 'Aún no tienes solicitudes de reparación.', 'en': 'No repair requests yet.'},
    'submit_repair_btn':{'es': 'Enviar Solicitud de Reparación', 'en': 'Submit a Repair Request'},
    'estimated_lbl':   {'es': 'Estimado:',     'en': 'Estimated:'},

    # Auth
    'welcome_back':    {'es': 'Bienvenido de vuelta', 'en': 'Welcome back'},
    'sign_in_sub':     {'es': 'Inicia sesión en tu cuenta SmartDrone', 'en': 'Sign in to your SmartDrone account'},
    'username_lbl':    {'es': 'Usuario',       'en': 'Username'},
    'password_lbl':    {'es': 'Contraseña',    'en': 'Password'},
    'sign_in_btn':     {'es': 'Iniciar Sesión','en': 'Sign In'},
    'no_account':      {'es': '¿No tienes cuenta?', 'en': 'No account?'},
    'create_one':      {'es': 'Créala aquí',   'en': 'Create one'},
    'create_account':  {'es': 'Crear Cuenta',  'en': 'Create Account'},
    'join_sub':        {'es': 'Únete a SmartDrone hoy', 'en': 'Join SmartDrone today'},
    'email_lbl2':      {'es': 'Correo',        'en': 'Email'},
    'confirm_pass':    {'es': 'Confirmar Contraseña', 'en': 'Confirm Password'},
    'create_btn':      {'es': 'Crear Cuenta',  'en': 'Create Account'},
    'have_account':    {'es': '¿Ya tienes cuenta?', 'en': 'Already have an account?'},
    'sign_in_link':    {'es': 'Inicia sesión', 'en': 'Sign in'},

    # Admin dashboard
    'dashboard_title': {'es': 'Panel de Administración', 'en': 'Admin Dashboard'},
    'manage_repairs':  {'es': 'Gestionar Reparaciones', 'en': 'Manage Repairs'},
    'drones_listed':   {'es': 'Drones Listados', 'en': 'Drones Listed'},
    'total_orders':    {'es': 'Pedidos Totales','en': 'Total Orders'},
    'total_revenue':   {'es': 'Ingresos Totales','en': 'Total Revenue'},
    'repair_requests': {'es': 'Solicitudes de Reparación', 'en': 'Repair Requests'},
    'pending_lbl':     {'es': 'pendientes',    'en': 'pending'},
    'recent_orders':   {'es': 'Pedidos Recientes', 'en': 'Recent Orders'},
    'recent_repairs':  {'es': 'Reparaciones Recientes', 'en': 'Recent Repairs'},
    'manage_all':      {'es': 'Gestionar Todo','en': 'Manage All'},
    'no_orders_yet':   {'es': 'Aún no hay pedidos.', 'en': 'No orders yet.'},
    'no_repairs_yet':  {'es': 'Aún no hay solicitudes.', 'en': 'No repair requests yet.'},
    'col_user':        {'es': 'Usuario',       'en': 'User'},

    # Admin repairs
    'admin_repairs_title': {'es': 'Gestionar Reparaciones', 'en': 'Manage Repairs'},
    'back_dashboard':  {'es': '← Panel',       'en': '← Dashboard'},
    'est_cost_field':  {'es': 'Costo Estimado ($)', 'en': 'Estimated Cost ($)'},
    'tech_notes_field':{'es': 'Notas del Técnico', 'en': 'Technician Notes'},
    'update_btn':      {'es': 'Actualizar',    'en': 'Update'},
    'view_btn':        {'es': 'Ver',           'en': 'View'},
    'no_repair_req':   {'es': 'Aún no hay solicitudes de reparación.', 'en': 'No repair requests yet.'},

    # Footer
    'footer_tagline':  {'es': '✦ Vuela Más Lejos. Repara Más Inteligente.', 'en': '✦ Fly Further. Repair Smarter.'},
    'footer_copy':     {'es': '© 2026 SmartDrone. Todos los derechos reservados.', 'en': '© 2026 SmartDrone. All rights reserved.'},
    'footer_desc':     {'es': 'Drones premium y servicios profesionales de reparación.', 'en': 'Premium drones & professional repair services.'},

    # Status labels
    'status_received':   {'es': 'Recibido',    'en': 'Received'},
    'status_diagnosing': {'es': 'Diagnosticando', 'en': 'Diagnosing'},
    'status_in_repair':  {'es': 'En Reparación','en': 'In Repair'},
    'status_ready':      {'es': 'Listo para Recoger', 'en': 'Ready for Pickup'},
    'status_delivered':  {'es': 'Entregado',   'en': 'Delivered'},
    'status_cancelled':  {'es': 'Cancelado',   'en': 'Cancelled'},

    # Order statuses
    'order_pending':   {'es': 'Pendiente',     'en': 'Pending'},
    'order_confirmed': {'es': 'Confirmado',    'en': 'Confirmed'},
    'order_shipped':   {'es': 'Enviado',       'en': 'Shipped'},
    'order_delivered': {'es': 'Entregado',     'en': 'Delivered'},
    'order_cancelled': {'es': 'Cancelado',     'en': 'Cancelled'},

    # Theme / lang toggle
    'dark_mode':       {'es': 'Oscuro',        'en': 'Dark'},
    'light_mode':      {'es': 'Claro',         'en': 'Light'},
    'lang_es':         {'es': 'ES',            'en': 'ES'},
    'lang_en':         {'es': 'EN',            'en': 'EN'},

    # Repair home items
    'drone_repair_items': {
        'es': ['Reemplazo de motor y ESC', 'Reparación de chasis y brazos', 'Calibración del controlador de vuelo', 'Problemas de batería y carga', 'Reparación de GPS y brújula', 'Actualizaciones de firmware'],
        'en': ['Motor & ESC replacement', 'Frame & arm repairs', 'Flight controller calibration', 'Battery & charging issues', 'GPS & compass fixes', 'Firmware updates'],
    },
    'camera_repair_items': {
        'es': ['Reparación de motor y cinta del gimbal', 'Reemplazo de lente', 'Limpieza del sensor de imagen', 'Ajuste de cámara FPV', 'Problemas de transmisión de video', 'Reparaciones de cámaras de acción (GoPro, DJI Osmo)'],
        'en': ['Gimbal motor & ribbon repair', 'Lens replacement', 'Image sensor cleaning', 'FPV camera tuning', 'Video transmission issues', 'Action cam repairs (GoPro, DJI Osmo)'],
    },
}


@register.simple_tag(takes_context=True)
def t(context, key):
    """Translate a key based on current session language."""
    lang = context.get('lang', 'es')
    entry = TRANSLATIONS.get(key, {})
    if isinstance(entry, dict) and 'es' in entry:
        return entry.get(lang, entry.get('es', key))
    return key


@register.simple_tag(takes_context=True)
def t_list(context, key):
    """Return a translated list."""
    lang = context.get('lang', 'es')
    entry = TRANSLATIONS.get(key, {})
    if isinstance(entry, dict):
        return entry.get(lang, entry.get('es', []))
    return []
