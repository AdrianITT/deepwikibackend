"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/campo/', include('campo.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='login'),
    path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
    path('empresa/', TemplateView.as_view(template_name='index.html'), name='empresa'),
    path('cliente/', TemplateView.as_view(template_name='index.html'), name='cliente'),
    path('EditarCliente/<int:id>/', TemplateView.as_view(template_name='index.html'), name='EditarCliente'),
    path('servicio/', TemplateView.as_view(template_name='index.html'), name='servicio'),
    path('crear_cotizacion/<int:id>/', TemplateView.as_view(template_name='index.html'), name='crear_cotizacion'),
    path('cotizar/', TemplateView.as_view(template_name='index.html'), name='cotizar'),
    path('detalles_cotizaciones/<int:id>/', TemplateView.as_view(template_name='index.html'), name='detalles_cotizaciones'),
    path('EditarCotizacion/<int:id>/', TemplateView.as_view(template_name='index.html'), name='EditarCotizacion'),
    path('proyectos/', TemplateView.as_view(template_name='index.html'), name='proyectos'),
    path('generar_orden/', TemplateView.as_view(template_name='index.html'), name='generar_orden'),
    path('DetalleOrdenTrabajo/<int:id>/', TemplateView.as_view(template_name='index.html'), name='DetalleOrdenTrabajo'),
    path('GenerarOrdenTrabajo/<int:id>/', TemplateView.as_view(template_name='index.html'), name='GenerarOrdenTrabajo'),
    path('usuario/', TemplateView.as_view(template_name='index.html'), name='usuario'),
    path('EditarUsuario/<int:id>/', TemplateView.as_view(template_name='index.html'), name='EditarUsuario'),
    path('configuracionorganizacion/', TemplateView.as_view(template_name='index.html'), name='configuracionorganizacion'),
    path('CargaCSD/', TemplateView.as_view(template_name='index.html'), name='CargaCSD'),
    path('factura/', TemplateView.as_view(template_name='index.html'), name='factura'),
    path('CrearFactura/<int:id>/', TemplateView.as_view(template_name='index.html'), name='CrearFactura'),
    path('detallesfactura/<int:id>/', TemplateView.as_view(template_name='index.html'), name='detallesfactura'),
    path('preCotizacion/', TemplateView.as_view(template_name='index.html'), name='preCotizacion'),
    path('CrearPreCotizacion/', TemplateView.as_view(template_name='index.html'), name='CrearPreCotizacion'),
    path('preCotizacionDetalles/<int:id>/', TemplateView.as_view(template_name='index.html'), name='preCotizacionDetalles'),
    path('Pagos/', TemplateView.as_view(template_name='index.html'), name='Pagos'),
    path('CrearPagos/', TemplateView.as_view(template_name='index.html'), name='CrearPagos'),
    path('CrearPagos/<int:id>/', TemplateView.as_view(template_name='index.html'), name='CrearPagos'),
]

# Sirviendo archivos estáticos correctamente
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 🔹 Agregar la ruta para manifest.json
urlpatterns += [
    re_path(r'^manifest.json$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'build'), 'path': 'manifest.json'}),
    re_path(r'^logo192.png$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'build'), 'path': 'logo192.png'}),
    re_path(r'^favicon.ico$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'build'), 'path': 'favicon.ico'}),
]


# Configuración para servir archivos de medios cuando DEBUG es False
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

