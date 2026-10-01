from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from philosophy.models import Argument
from projects.models import Project
from core.models import AboutPage

class Command(BaseCommand):
    help = "Populate initial template entries and default admin user if needed"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@hudisthinking.com', 'adminpass123')
            self.stdout.write(self.style.SUCCESS("Superuser created: username 'admin' | password 'adminpass123' (Remember to change password)"))

        # Initial About Page placeholder
        if not AboutPage.objects.exists():
            AboutPage.objects.create(
                title="About HudIsThinking LLC",
                content="HudIsThinking LLC.\n\nPersonal archive of philosophical arguments, written manuscripts, and software works.\n\n[Content placeholder — easily edited in Django Admin.]",
                meta_description="HudIsThinking LLC. Personal archive of philosophical arguments and software works."
            )
            self.stdout.write(self.style.SUCCESS("Created initial About Page template entry."))

        # Template Philosophy Argument
        if not Argument.objects.exists():
            Argument.objects.create(
                title="On the Indivisibility of Computational Agency",
                slug="on-the-indivisibility-of-computational-agency",
                category="argument",
                thesis="Agency cannot be decomposed into passive algorithmic steps without discarding intentionality.",
                content="""## Proposition I

Any model that purports to explain agency must account for self-directed intentionality rather than mere statistical mimicry.

### Premise 1
A mechanical sequence of state transitions possesses syntax but not intrinsic semantics.

### Premise 2
Agency requires semantic orientation towards states of affairs.

### Conclusion
Pure syntactic computation does not suffice for genuine agency without external grounding.

---
*[This is a template entry. Replace or remove via the Admin dashboard at `/admin/`.]*""",
                meta_description="A philosophical inquiry into computational agency and intentionality.",
                meta_keywords="philosophy, agency, computation, mind"
            )
            self.stdout.write(self.style.SUCCESS("Created template Philosophy argument entry."))

        # Template Project
        if not Project.objects.exists():
            Project.objects.create(
                title="Core Protocol Prototype",
                slug="core-protocol-prototype",
                project_type="game",
                tagline="Experimental standalone interactive software build.",
                description="""### Overview
Experimental build exploring minimalist mechanics and systems.

### Controls
- **Movement**: Arrow Keys / WASD
- **Action**: Space
- **Exit**: Esc

### Notes
Packaged as a standalone executable. Run directly without installation.

---
*[This is a template entry. Upload your actual `.exe` or `.zip` files and edit this text via `/admin/`.]*""",
                version="0.1.0",
                platform="Windows x64",
                system_requirements="Windows 10/11 64-bit",
                meta_description="Experimental standalone software build by HudIsThinking."
            )
            self.stdout.write(self.style.SUCCESS("Created template Project entry."))

        self.stdout.write(self.style.SUCCESS("Site setup completed successfully."))
