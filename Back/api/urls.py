from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views


router = routers.DefaultRouter()
router.register(r'machines', views.MachineViewSet)
router.register(r'maintenances', views.MaintenanceViewSet)
router.register(r'claims', views.ClaimViewSet)

urlpatterns = [
    path('catalogs/', views.CatalogsView.as_view(), name='Catalogs'),
    path('catalogs/<str:category>/', views.CatalogView.as_view(), name='Catalog'),
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),    
]