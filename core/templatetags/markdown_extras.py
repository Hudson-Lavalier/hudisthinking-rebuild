import re
from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_filter(text):
    if not text:
        return ""

    # 1. Strip broken WordPress/remote uploads and placeholder image tags as requested
    clean_text = re.sub(
        r'<img\b[^>]*(?:hudisthinking\.com/wp-content|/projects/Images4Bat|elementor/assets)[^>]*>',
        '',
        text,
        flags=re.IGNORECASE
    )
    # 2. If legacy WordPress content contains accordions, strip Elementor's duplicate text dump following the last </details> tag
    last_details = list(re.finditer(r'</details>', clean_text, re.IGNORECASE))
    if last_details:
        clean_text = clean_text[:last_details[-1].end()]

    # 3. Normalize whitespace-only lines so empty tabs don't trigger phantom blocks
    clean_text = re.sub(r'^[ \t]+$', '', clean_text, flags=re.MULTILINE)

    # 3. Strip leading indentation before HTML tags so markdown treats them as HTML rather than code blocks
    clean_text = re.sub(
        r'^[ \t]+(<(?:details|summary|p|h[1-6]|div|a|style|ul|ol|li|table|thead|tbody|tr|th|td|blockquote|section|header|footer|span|strong|em|b|i)\b)',
        r'\1',
        clean_text,
        flags=re.MULTILINE | re.IGNORECASE
    )

    # 4. Configure Python-Markdown
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
        ]
    )
    # Deregister 4-space indented code blocks to prevent HTML indentation from rendering as code boxes
    md.parser.blockprocessors.deregister('code')

    html = md.convert(clean_text)
    return mark_safe(html)

