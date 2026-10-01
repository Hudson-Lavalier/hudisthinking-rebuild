import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.decorators.csrf import ensure_csrf_cookie
from core.templatetags.markdown_extras import markdown_filter
from core.models import MediaItem

# Allowed models and their whitelisted editable fields for in-situ editing
EDITABLE_WHITELIST = {
    'philosophy.argument': {'title', 'thesis', 'content', 'justifications', 'references', 'is_published'},
    'core.custompage': {'title', 'content', 'meta_description', 'is_published'},
    'core.aboutpage': {'title', 'content', 'meta_description'},
    'core.siteconfiguration': {'site_title', 'tagline', 'meta_description'},
    'projects.project': {'title', 'tagline', 'description', 'platform', 'version', 'is_published'},
}

def staff_required(view_func):
    """Ensure user is logged in and is staff."""
    def _wrapped(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            return JsonResponse({'status': 'error', 'message': 'Authentication required (staff only).'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped

@require_POST
@staff_required
def live_save(request):
    """
    In-situ live editor save endpoint.
    Accepts JSON payload:
    {
        "model": "philosophy.argument",
        "id": 1,
        "fields": {
            "title": "New Title",
            "content": "# New Markdown Content"
        }
    }
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Invalid JSON payload: {str(e)}'}, status=400)

    model_key = data.get('model', '').strip().lower()
    object_id = data.get('id')
    fields_data = data.get('fields', {})

    if model_key not in EDITABLE_WHITELIST:
        return JsonResponse({
            'status': 'error',
            'message': f'Model {model_key} is not registered for live in-situ editing.'
        }, status=400)

    allowed_fields = EDITABLE_WHITELIST[model_key]
    invalid_fields = set(fields_data.keys()) - allowed_fields
    if invalid_fields:
        return JsonResponse({
            'status': 'error',
            'message': f'Unauthorized fields for model {model_key}: {list(invalid_fields)}'
        }, status=400)

    try:
        app_label, model_name = model_key.split('.')
        model_cls = apps.get_model(app_label, model_name)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Model lookup failed: {str(e)}'}, status=400)

    try:
        obj = model_cls.objects.get(pk=object_id)
    except model_cls.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f'Object {object_id} not found.'}, status=404)

    # Update whitelisted fields
    rendered_fields = {}
    for field_name, field_value in fields_data.items():
        setattr(obj, field_name, field_value)
        # If this field is markdown content, provide the server-rendered HTML preview back
        if field_name in ('content', 'justifications', 'references', 'description'):
            rendered_fields[field_name] = markdown_filter(field_value)

    try:
        obj.full_clean()
    except ValidationError as ve:
        return JsonResponse({'status': 'error', 'message': 'Validation failed', 'errors': ve.message_dict}, status=400)

    obj.save()

    return JsonResponse({
        'status': 'success',
        'message': f'Saved {model_key} #{object_id} successfully.',
        'updated_fields': list(fields_data.keys()),
        'rendered_previews': rendered_fields,
    })


@require_GET
@staff_required
def live_media_list(request):
    """
    Returns media library items for in-situ insertion.
    """
    query = request.GET.get('q', '').strip()
    media_qs = MediaItem.objects.all().order_by('-uploaded_at')
    if query:
        media_qs = media_qs.filter(title__icontains=query)

    items = []
    for m in media_qs[:40]:
        items.append({
            'id': m.id,
            'title': m.title,
            'url': m.file.url if m.file else '',
            'media_type': m.media_type,
            'file_size': m.file_size_display,
            'markdown_embed': m.markdown_embed,
        })

    return JsonResponse({
        'status': 'success',
        'items': items,
    })
