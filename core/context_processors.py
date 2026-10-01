from .models import SiteConfiguration, NavigationItem

def site_context(request):
    try:
        config = SiteConfiguration.get_solo()
    except Exception:
        config = None

    site_name = config.site_title if config else 'HudIsThinking'
    llc_name = config.llc_name if config else 'HudIsThinking LLC'
    site_desc = config.tagline if config else 'Personal archive of philosophical arguments and software works.'

    try:
        header_nav = list(NavigationItem.objects.filter(location='header', is_active=True).order_by('order'))
        footer_nav = list(NavigationItem.objects.filter(location='footer', is_active=True).order_by('order'))
    except Exception:
        header_nav = []
        footer_nav = []

    return {
        'site_config': config,
        'SITE_NAME': site_name,
        'LLC_NAME': llc_name,
        'SITE_DESCRIPTION': site_desc,
        'header_nav_items': header_nav,
        'footer_nav_items': footer_nav,
    }
