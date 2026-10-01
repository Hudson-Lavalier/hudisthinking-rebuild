from django.template.loaders.base import Loader
from django.template import Origin, TemplateDoesNotExist

class DatabaseTemplateLoader(Loader):
    """
    Template loader that loads template code directly from the DBTemplate model.
    If no active DBTemplate exists with the requested name, raises TemplateDoesNotExist
    so Django cleanly falls back to the filesystem and app template loaders.
    """
    def get_template_sources(self, template_name):
        yield Origin(
            name=f"db:{template_name}",
            template_name=template_name,
            loader=self,
        )

    def get_contents(self, origin):
        try:
            from core.models import DBTemplate
            db_template = DBTemplate.objects.filter(
                name=origin.template_name,
                is_active=True
            ).first()
            if db_template and db_template.content:
                return db_template.content
        except Exception:
            # During migrations or before DB is ready, gracefully pass
            pass
        raise TemplateDoesNotExist(origin)
