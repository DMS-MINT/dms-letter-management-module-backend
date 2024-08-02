from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core.common.admin import dms_admin_site
from core.puppeteer.views import display_letter, generate_pdf

urlpatterns = [
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("dms-admin/", dms_admin_site.urls),
    path("admin/", admin.site.urls),
    path("api/", include(("core.api.urls", "api"), namespace="api")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("generate-pdf/", generate_pdf, name="generate_pdf"),
    path("display-letter/", display_letter, name="display-letter"),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from config.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa

urlpatterns = DebugToolbarSetup.do_urls(urlpatterns)

websocket_urlpatterns = []
