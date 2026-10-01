from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from philosophy.models import Argument, PhilosophyCategory, PhilosophyTag
from projects.models import Project, ProjectCategory
from core.models import AboutPage, SiteConfiguration, NavigationItem

class Command(BaseCommand):
    help = "Populate initial template entries, site configuration, categories, and default navigation"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('hud', 'hud@hudisthinking.com', 'hd63^7387^#hGTe66URJ2*73917HG41284A')
            self.stdout.write(self.style.SUCCESS("Superuser 'hud' created."))

        # 1. Site Configuration
        config, created = SiteConfiguration.objects.get_or_create(id=1, defaults={
            'site_title': 'HudIsThinking',
            'llc_name': 'HudIsThinking LLC',
            'tagline': 'Personal archive of philosophical arguments and software works.',
            'enable_wisps': True,
            'wisp_count': 16,
            'wisp_speed': 0.08,
        })
        if created:
            self.stdout.write(self.style.SUCCESS("Initialized Site Configuration."))

        # 2. Navigation Items
        default_nav = [
            ('Philosophy', '/philosophy/', 'header', 1),
            ('Projects', '/projects/', 'header', 2),
            ('About', '/about/', 'header', 3),
            ('Home', '/', 'footer', 1),
            ('Philosophy', '/philosophy/', 'footer', 2),
            ('Projects', '/projects/', 'footer', 3),
            ('About', '/about/', 'footer', 4),
        ]
        for label, url, loc, order in default_nav:
            NavigationItem.objects.get_or_create(
                label=label, location=loc,
                defaults={'url': url, 'order': order, 'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS("Initialized default navigation items."))

        # 3. Philosophy Categories
        cat_arg, _ = PhilosophyCategory.objects.get_or_create(
            slug='arguments',
            defaults={'name': 'Arguments', 'order': 1}
        )
        cat_essay, _ = PhilosophyCategory.objects.get_or_create(
            slug='essays',
            defaults={'name': 'Essays', 'order': 2}
        )
        cat_frag, _ = PhilosophyCategory.objects.get_or_create(
            slug='fragments',
            defaults={'name': 'Fragments', 'order': 3}
        )

        # 4. Project Categories
        type_game, _ = ProjectCategory.objects.get_or_create(
            slug='games',
            defaults={'name': 'Games', 'order': 1}
        )
        type_exe, _ = ProjectCategory.objects.get_or_create(
            slug='executables',
            defaults={'name': 'Executables', 'order': 2}
        )
        type_proto, _ = ProjectCategory.objects.get_or_create(
            slug='prototypes',
            defaults={'name': 'Prototypes', 'order': 3}
        )

        # 5. Philosophy Tags
        tag_ethics, _ = PhilosophyTag.objects.get_or_create(slug='ethics', defaults={'name': 'Ethics'})
        tag_metaethics, _ = PhilosophyTag.objects.get_or_create(slug='meta-ethics', defaults={'name': 'Meta-Ethics'})
        tag_metaphysics, _ = PhilosophyTag.objects.get_or_create(slug='metaphysics', defaults={'name': 'Metaphysics'})
        tag_freewill, _ = PhilosophyTag.objects.get_or_create(slug='free-will', defaults={'name': 'Free Will'})
        tag_epistemology, _ = PhilosophyTag.objects.get_or_create(slug='epistemology', defaults={'name': 'Epistemology'})
        tag_mind, _ = PhilosophyTag.objects.get_or_create(slug='philosophy-of-mind', defaults={'name': 'Philosophy of Mind'})
        tag_logic, _ = PhilosophyTag.objects.get_or_create(slug='logic', defaults={'name': 'Logic'})

        # 6. About Page placeholder
        if not AboutPage.objects.exists():
            AboutPage.objects.create(
                title="About HudIsThinking LLC",
                content="HudIsThinking LLC.\n\nPersonal archive of philosophical arguments, written manuscripts, and software works.\n\n[Content placeholder — easily edited in Django Admin.]",
                meta_description="HudIsThinking LLC. Personal archive of philosophical arguments and software works."
            )
            self.stdout.write(self.style.SUCCESS("Created initial About Page template entry."))

        # 7. Template Philosophy Argument
        if not Argument.objects.exists():
            arg = Argument.objects.create(
                title="On the Indivisibility of Computational Agency",
                slug="on-the-indivisibility-of-computational-agency",
                category=cat_arg,
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
            arg.tags.add(tag_mind, tag_metaphysics, tag_freewill)
            self.stdout.write(self.style.SUCCESS("Created template Philosophy argument entry with tags."))

        # 8. Template Project
        if not Project.objects.exists():
            Project.objects.create(
                title="Core Protocol Prototype",
                slug="core-protocol-prototype",
                project_type=type_game,
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
