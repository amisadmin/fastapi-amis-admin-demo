from core.settings import settings
from fastapi_amis_admin import i18n

i18n.set_language(settings.language)
