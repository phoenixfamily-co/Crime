"""
URL configuration for CrimeProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from CrimeProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # مسیر پنل ادمین
    path('set_language/', include('django.conf.urls.i18n')),  # مسیر تغییر زبان
    path('not-supported/', TemplateView.as_view(template_name='support.html'), name='not_supported'),

]

urlpatterns += i18n_patterns(
    path('home/', include('Home.urls', namespace='home')),  # مسیر URLهای اپلیکیشن Home
    path('product/', include('Product.urls', namespace='product')),  # مسیر URLهای اپلیکیشن product
    path('play/', include('Play.urls', namespace='play')),  # مسیر URLهای اپلیکیشن play
    path('user/', include('User.urls', namespace='user')),  # مسیر URLهای اپلیکیشن user
    path('login/', include('Login.urls', namespace='login')),  # مسیر URLهای اپلیکیشن login

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
