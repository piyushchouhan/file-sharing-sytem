from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup", views.client_user_signup, name="client_user_signup"),
    path("signin", views.client_user_signin, name="client_user_signin"),
    path("download-file/<int:file_id>/", views.download_file_view, name="download_file"),
    path("files/", views.file_list_view, name="file_list"),
    path('accounts/', include('allauth.urls')),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='account_confirm_email'),
    path('email-sent/', views.email_sent, name='account_email'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)