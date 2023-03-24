from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import EmailSenderView, TaskModelViewSet

router = SimpleRouter()
router.register("tasks", TaskModelViewSet, basename="tasks")


urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("rest-auth/", include("accounts.urls")),
    path("rest-auth/", include("dj_rest_auth.urls")),
    # this url is used to generate email content
    re_path(
        r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
        EmailSenderView.as_view(),
        name="password_reset_confirm",
    ),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
] + router.urls
