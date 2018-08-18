"""tree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from shop import views
from django.contrib.auth import views as authViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='Home'),
    path('shop/', include('shop.urls')),
    path('search/', include('search_app.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('account/create/', views.signupView, name='signup'),
    path('account/login/', views.signinView, name='signin'),
    path('account/logout/', views.signoutView, name='signout'),
    re_path(r'^account/password_reset/$', authViews.password_reset, {'template_name' : 'accounts/reset_password.html' }, name='password_reset'),
    re_path(r'^account/password_reset/done/$', authViews.password_reset_done, {'template_name': 'accounts/reset_password_done.html'}, name='password_reset_done'),
    re_path(r'^account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', authViews.password_reset_confirm, {'template_name': 'accounts/reset_password_confirm.html'}, name='password_reset_confirm'),
    re_path(r'^account/reset/done/$', authViews.password_reset_complete, {'template_name': 'accounts/reset_done.html'}, name='password_reset_complete'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)