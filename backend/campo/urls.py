from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PreservadorViewSet, MatrizViewSet, ClaveViewSet, ContenedorViewSet, ParametroViewSet
from .views import PrioridadViewSet, CustodiaExternaViewSet, MuestraViewSet, RegistroCustodiaViewSet
from .views import FiltroViewSet, PreservadorMuestraViewSet, llenar_excel_con_informacion, EstadoCustodiaViewSet
from .views import custodiaexternadata, llenar_excel_con_informacion2, allcustodiaexterna

router = DefaultRouter()
router.register(r'preservador', PreservadorViewSet)
router.register(r'matriz', MatrizViewSet)
router.register(r'clave', ClaveViewSet)
router.register(r'contenedor', ContenedorViewSet)
router.register(r'parametro', ParametroViewSet)
router.register(r'prioridad', PrioridadViewSet)
router.register(r'custodiaexterna', CustodiaExternaViewSet)
router.register(r'muestra', MuestraViewSet)
router.register(r'registrocustodia', RegistroCustodiaViewSet)
router.register(r'filtro', FiltroViewSet)
router.register(r'preservadormuestra', PreservadorMuestraViewSet)
router.register(r'estadocustodia', EstadoCustodiaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('llenar_excel_con_informacion/<int:custodia_id>/', llenar_excel_con_informacion, name='llenar_excel_con_informacion'),
    path('llenar_excel_con_informacion2/<int:custodia_id>/', llenar_excel_con_informacion2, name='llenar_excel_con_informacion2'),
    path('custodiaexternadata/<int:custodia_id>/', custodiaexternadata, name='custodiaexternadata'),
    path('allcustodiaexterna/', allcustodiaexterna, name='allcustodiaexterna'),
]
