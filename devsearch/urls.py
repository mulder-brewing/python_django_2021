"""devsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('', include('users.urls')),

    path('reset-password', auth_views.PasswordResetView.as_view(template_name='reset_password.html'),
         name='password_reset'),
    path('reset-password-email-sent',
         auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'),
         name='password_reset_done'),
    path('reset-password/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='enter_new_password.html'),
         name='password_reset_confirm'),
    path('reset-password-complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'),
         name='password_reset_complete')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
