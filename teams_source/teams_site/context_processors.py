from django.conf import settings

def info(request):
    return {'PRODUCTION_UI': settings.PRODUCTION_UI, "NAME": settings.NAME, "VERSION": settings.VERSION}