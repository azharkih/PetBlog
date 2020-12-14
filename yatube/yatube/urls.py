from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler403 = "apps.posts.views.page_forbidden"
handler404 = "apps.posts.views.page_not_found"
handler500 = "apps.posts.views.server_error"

urlpatterns = [
    # раздел администратора
    path('admin/', admin.site.urls),
    # flatpages
    path('about-author/', views.flatpage, {'url': '/about-author/'},
         name='about-author'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'},
         name='about-spec'),
    path('about/', include('django.contrib.flatpages.urls')),
    # регистрация и авторизация
    path('auth/', include('apps.users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    # импорт из приложения posts
    path('', include('apps.posts.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
