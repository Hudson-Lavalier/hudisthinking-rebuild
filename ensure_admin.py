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

if __name__ == '__main__':
    ensure_superusers()
