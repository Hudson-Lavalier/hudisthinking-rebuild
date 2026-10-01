import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

def ensure_superusers():
    User = get_user_model()
    # Read admin credentials from environment or fallback to user requested
    admin_user = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'hud')
    admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'hudson.amaral11@gmail.com')
    admin_pwd = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'bFtv3jkYa6d2drn')

    for uname in [admin_user, 'admin']:
        user, created = User.objects.get_or_create(
            username=uname,
            defaults={'email': admin_email, 'is_staff': True, 'is_superuser': True}
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(admin_pwd)
        user.save()
        status = "Created" if created else "Updated"
        print(f"[{status}] Superuser '{uname}' active with configured password.")

def ensure_content():
    from core.models import SiteConfiguration, AboutPage, ConnectPage, DBTemplate
    from pathlib import Path
    from django.conf import settings

    SiteConfiguration.get_solo()
    AboutPage.get_solo()
    ConnectPage.get_solo()

    # Pre-populate DBTemplate catalog from filesystem
    template_names = [
        'about.html',
        'connect.html',
        'home.html',
        'custom_page.html',
        'philosophy/list.html',
        'philosophy/detail.html',
        'projects/list.html',
        'projects/detail.html',
    ]
    for t_name in template_names:
        fs_path = Path(settings.BASE_DIR) / 'templates' / t_name
        content = ""
        if fs_path.exists():
            try:
                content = fs_path.read_text(encoding='utf-8')
            except Exception:
                pass
        t_obj, created = DBTemplate.objects.get_or_create(
            name=t_name,
            defaults={
                'description': f"Template for {t_name}",
                'content': content,
                'is_active': False,
            }
        )
        if not t_obj.content and content:
            t_obj.content = content
            t_obj.save()
    print("[Success] Content singletons and DBTemplate catalog initialized.")

if __name__ == '__main__':
    ensure_superusers()
    ensure_content()

