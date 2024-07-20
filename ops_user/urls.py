from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'files', views.UploadedFileViewSet)

urlpatterns = [
    path("", views.ops_user_index, name="index"),
    path("ops/signup", views.ops_user_signup, name="ops_user_signup"),
    path("ops/signin", views.ops_user_signin, name="ops_user_signin"),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)