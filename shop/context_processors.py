def ui_settings(request):
    """Inject lang and theme into every template context."""
    lang = request.session.get('lang', 'es')
    theme = request.session.get('theme', 'dark')
    return {'lang': lang, 'theme': theme}
