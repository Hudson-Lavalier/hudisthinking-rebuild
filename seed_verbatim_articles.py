# Import script that seeds the verbatim articles into Django models
import os
import sys
import json
import re

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from philosophy.models import Argument, PhilosophyCategory, PhilosophyTag
from projects.models import Project, ProjectCategory

with open('extracted_verbatim_articles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ensure Categories exist
cat_args, _ = PhilosophyCategory.objects.get_or_create(
    slug='arguments',
    defaults={'name': 'Arguments', 'order': 1, 'description': 'Formal philosophical arguments and treatises.'}
)
cat_games, _ = ProjectCategory.objects.get_or_create(
    slug='games',
    defaults={'name': 'Games & Interactive', 'order': 1, 'description': 'Interactive games and prototypes.'}
)
cat_tools, _ = ProjectCategory.objects.get_or_create(
    slug='desktop-tools',
    defaults={'name': 'Desktop Tools', 'order': 2, 'description': 'Native desktop applications and companions.'}
)

# Ensure Tags exist
tag_meta, _ = PhilosophyTag.objects.get_or_create(slug='metaphysics', defaults={'name': 'Metaphysics'})
tag_epist, _ = PhilosophyTag.objects.get_or_create(slug='epistemology', defaults={'name': 'Epistemology'})
tag_theology, _ = PhilosophyTag.objects.get_or_create(slug='philosophy-of-religion', defaults={'name': 'Philosophy of Religion'})
tag_freewill, _ = PhilosophyTag.objects.get_or_create(slug='free-will', defaults={'name': 'Free Will'})
tag_ethics, _ = PhilosophyTag.objects.get_or_create(slug='ethics', defaults={'name': 'Ethics'})

def sanitize_content(raw_html):
    # Strip broken WordPress image embeds and theme placeholders
    c = re.sub(r'<img\b[^>]*(?:hudisthinking\.com/wp-content|/projects/Images4Bat|elementor/assets)[^>]*>', '', raw_html, flags=re.IGNORECASE)
    c = re.sub(r'<img\b[^>]*\bsrc=[\'"]\s*[\'"][^>]*>', '', c, flags=re.IGNORECASE)

    # If article contains accordions (<details>), Elementor appended an unstyled duplicate dump of all accordion contents after the last </details> tag.
    # Truncate at the last </details> tag to eliminate the duplicate text dump.
    last_details = list(re.finditer(r'</details>', c, re.IGNORECASE))
    if last_details:
        c = c[:last_details[-1].end()]

    # Normalize whitespace-only lines
    c = re.sub(r'^[ \t]+$', '', c, flags=re.MULTILINE)
    # Strip leading tabs/spaces before HTML tags so markdown processes them as HTML
    c = re.sub(r'^[ \t]+(<(?:details|summary|p|h[1-6]|div|a|style|ul|ol|li|table|thead|tbody|tr|th|td|blockquote|section|header|footer|span|strong|em|b|i)\b)', r'\1', c, flags=re.MULTILINE | re.IGNORECASE)
    return c.strip()

# 1. THE ARGUMENT FROM SPIRITUAL NON-CONVERGENCE
art_snc = data['the-argument-from-spiritual-non-convergence']
raw_snc = art_snc['content']
clean_snc = sanitize_content(raw_snc)

# Extract citation string from footer if present
cite_apa_snc = 'Amaral, H. J. (2026). The Argument from Spiritual Non-Convergence (Version 1.0). HudIsThinking LLC. https://hudisthinking.com/philosophy/the-argument-from-spiritual-non-convergence/'
cite_mla_snc = 'Amaral, Hudson J. "The Argument from Spiritual Non-Convergence." Hud Is Thinking, Version 1.0, 11 June 2026, https://hudisthinking.com/philosophy/the-argument-from-spiritual-non-convergence/.'

arg1, created = Argument.objects.update_or_create(
    slug='the-argument-from-spiritual-non-convergence',
    defaults={
        'title': 'The Argument from Spiritual Non-Convergence',
        'category': cat_args,
        'published_date': '2026-06-12',
        'thesis': 'The classical theistic worldview proposes observable spiritual interactions, yet empirical spiritual practices and anomalous experiences fail to epistemically converge upon a coherent ontological reality.',
        'content': clean_snc,
        'citation_apa': cite_apa_snc,
        'citation_mla': cite_mla_snc,
        'is_published': True,
    }
)
arg1.tags.set([tag_epist, tag_theology, tag_meta])
print(f"Seeded: {arg1.title} (Created={created}, Len={len(arg1.content)})")


# 2. WHY GOD IS ULTIMATELY RESPONSIBLE FOR SIN'S OCCURRENCE
art_sin = data['why-god-is-ultimately-responsible-for-sins-occurrence']
raw_sin = art_sin['content']
clean_sin = sanitize_content(raw_sin)

cite_apa_sin = "Amaral, H. J. (2026). Why God Is Ultimately Responsible for Sin's Occurrence: Divine Responsibility for the Occurrence of Sin (Version 1.0). HudIsThinking LLC. https://hudisthinking.com/philosophy/why-god-is-ultimately-responsible-for-sins-occurrence/"
cite_mla_sin = 'Amaral, Hudson J. "Why God Is Ultimately Responsible for Sin\'s Occurrence." Hud Is Thinking, Version 1.0, 11 June 2026, https://hudisthinking.com/philosophy/why-god-is-ultimately-responsible-for-sins-occurrence/.'

arg2, created = Argument.objects.update_or_create(
    slug='why-god-is-ultimately-responsible-for-sins-occurrence',
    defaults={
        'title': "Why God Is Ultimately Responsible for Sin's Occurrence",
        'category': cat_args,
        'published_date': '2026-06-12',
        'thesis': 'Under classical theism, divine upstream actualization, exhaustive foreknowledge, and sovereign creation establish ultimate responsibility for the occurrence and conditions of sin.',
        'content': clean_sin,
        'citation_apa': cite_apa_sin,
        'citation_mla': cite_mla_sin,
        'is_published': True,
    }
)
arg2.tags.set([tag_theology, tag_ethics, tag_meta])
print(f"Seeded: {arg2.title} (Created={created}, Len={len(arg2.content)})")


# 3. ARCHITECTURAL ESTABLISHISM - A TAKE ON PREDETERMINISM
art_arch = data['architectural-establishism-a-take-on-predeterminism']
raw_arch = art_arch['content']
clean_arch = sanitize_content(raw_arch)

cite_apa_arch = "Amaral, H. J. (2025). Architectural Establishism: A Take on Predeterminism (Version 1.0). HudIsThinking LLC. https://hudisthinking.com/philosophy/architectural-establishism-a-take-on-predeterminism/"
cite_mla_arch = 'Amaral, Hudson J. "Architectural Establishism - A Take on Predeterminism." Hud is Thinking, Version 1.0, 31 Dec. 2025, https://hudisthinking.com/philosophy/architectural-establishism-a-take-on-predeterminism/.'

arg3, created = Argument.objects.update_or_create(
    slug='architectural-establishism-a-take-on-predeterminism',
    defaults={
        'title': 'Architectural Establishism - A Take On Predeterminism',
        'category': cat_args,
        'published_date': '2025-12-31',
        'thesis': 'A formal metaphysical argument establishing how upstream divine architecture and essence factors deterministically govern agentic deliberation webs and ultimate outcomes.',
        'content': clean_arch,
        'citation_apa': cite_apa_arch,
        'citation_mla': cite_mla_arch,
        'is_published': True,
    }
)
arg3.tags.set([tag_freewill, tag_meta, tag_theology])
print(f"Seeded: {arg3.title} (Created={created}, Len={len(arg3.content)})")


# 4. DESKTOP BUDDY COMPANION (Project)
art_desk = data['desktop-buddy-companion']
raw_desk = art_desk['content']
clean_desk = sanitize_content(raw_desk)

proj1, created = Project.objects.update_or_create(
    slug='desktop-buddy-companion',
    defaults={
        'title': 'Desktop Buddy Companion',
        'project_type': cat_tools,
        'tagline': 'An interactive bat companion that lives directly on your Windows desktop with animations, games, and hunger systems.',
        'description': clean_desk,
        'version': '1.0.0',
        'platform': 'Windows x64',
        'system_requirements': 'Windows 10 / Windows 11',
        'show_download_button': True,
        'is_published': True,
        'release_date': '2026-08-09',
    }
)
print(f"Seeded: {proj1.title} (Created={created}, Len={len(proj1.description)})")


# 5. TERMINAL TRADER GAME (Project)
art_tt = data['terminal-trader-game']
raw_tt = art_tt['content']
clean_tt = sanitize_content(raw_tt)

proj2, created = Project.objects.update_or_create(
    slug='terminal-trader-game',
    defaults={
        'title': 'Terminal Trader Game',
        'project_type': cat_games,
        'tagline': 'A high-stakes retro financial terminal simulation and trading game for Windows and Android.',
        'description': clean_tt,
        'version': '1.0.4',
        'platform': 'Windows x64 & Android',
        'system_requirements': 'Windows 10/11 x64 or Android 8.0+',
        'show_download_button': True,
        'is_published': True,
        'release_date': '2026-03-27',
    }
)
print(f"Seeded: {proj2.title} (Created={created}, Len={len(proj2.description)})")

print("\n--- ALL VERBATIM ARTICLES SUCCESSFULLY SEEDED INTO DJANGO! ---")
