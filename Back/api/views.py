from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as django_filters
from django.db.models import Q

from .models import (Catalog, Machine, Maintenance, Claim)
from accounts.models import (User)
from .filters import (MachineFilter, MaintenanceFilter, ClaimFilter)
from .serializers import (CatalogSerializer, MachineSerializer, MachineDetailSerializer, MaintenanceSerializer, MaintenanceDetailSerializer, ClaimSerializer, ClaimDetailSerializer)
from .permissions import (MachinePermission, MaintenancePermission, ClaimPermission)


@extend_schema(tags=['Каталоги'])
@extend_schema_view(
    get=extend_schema(
        summary='Cписок категорий',
    )
)
class CatalogsView(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request):
        return Response(Catalog.CATEGORY_CHOISES)



@extend_schema(tags=['Каталоги'])
@extend_schema_view(
    get=extend_schema(
        summary='Содержимое каталога',
        parameters=[
            OpenApiParameter(name='category', location='path', type=OpenApiTypes.STR, required=True, description='Категория', enum=['tec', 'eng', 'trm', 'lda', 'sta', 'man', 'mfn', 'rec', 'sco'])
        ]
    )
)
class CatalogView(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request, category):
        catalog = Catalog.objects.filter(category=category)
        serializer = CatalogSerializer(catalog, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Техника'])
@extend_schema_view(
    list=extend_schema(
        summary='Список техники',
        parameters=[
            OpenApiParameter(name='serial', location='query', type=OpenApiTypes.STR, required=False, description='Зав. номер'),
            OpenApiParameter(name='tec', location='query', type=OpenApiTypes.NUMBER, required=False, description='модель техники'),
            OpenApiParameter(name='eng', location='query', type=OpenApiTypes.NUMBER, required=False, description='модель двигателя'),
            OpenApiParameter(name='trm', location='query', type=OpenApiTypes.NUMBER, required=False, description='модель трансмиссии'),
            OpenApiParameter(name='lda', location='query', type=OpenApiTypes.NUMBER, required=False, description='модель ведущего моста'),
            OpenApiParameter(name='sta', location='query', type=OpenApiTypes.NUMBER, required=False, description='модель управляемого моста'),
        ],
    ),
    retrieve=extend_schema(
        summary='Детальная информация о технике',
    )
)
class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all().order_by('serial')
    serializer_class = MachineSerializer
    filter_backends = (django_filters.DjangoFilterBackend, )
    filterset_class = MachineFilter
    
    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return MachineDetailSerializer(*args, **kwargs)
        return MachineSerializer(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == User.CLIENT:
                return Machine.objects.filter(client=user).order_by('shipment_date')
            elif user.role == User.SERVICE_COMPANY:
                return Machine.objects.filter(service_company=user).order_by('shipment_date')
            else:
                return Machine.objects.all().order_by('shipment_date') # для менеджеров
        return Machine.objects.all().order_by('serial')
    
    def get_permissions(self, *args, **kwargs):
        if self.action in ['list', 'retrieve', ]:
            return [AllowAny(*args, **kwargs), ]
        return [MachinePermission(*args, **kwargs), ]


@extend_schema(tags=['Техобслуживание'])
@extend_schema_view(
    list=extend_schema(
        summary='Список техобслуживания (для авторизованных пользователей)',
        parameters=[
            OpenApiParameter(name='serial', location='query', type=OpenApiTypes.STR, required=False, description='Зав. номер'),
            OpenApiParameter(name='service_company_id', location='query', type=OpenApiTypes.INT64, required=False, description='сервисная компания'),
            OpenApiParameter(name='man', location='query', type=OpenApiTypes.INT64, required=False, description='вид ТО'),
        ]
    ),
    retrieve=extend_schema(
        summary='Детальная информация о техобслуживании (для авторизованных пользователей)',
    )
)
class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    filter_backends = (django_filters.DjangoFilterBackend, )
    filterset_class = MaintenanceFilter
    permission_classes = [MaintenancePermission, ]
    
    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return MaintenanceDetailSerializer(*args, **kwargs)
        return MaintenanceSerializer(*args, **kwargs)
        
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == User.CLIENT:
                return Maintenance.objects.filter(machine__client=user).order_by('maintenance_date')
            elif user.role == User.SERVICE_COMPANY:
                return Maintenance.objects.filter(Q(machine__service_company=user) | Q(service_company=user)).order_by('maintenance_date')
            else:
                return Maintenance.objects.all().order_by('maintenance_date') # для менеджеров
        return Maintenance.objects.none()


@extend_schema(tags=['Ремонты'])
@extend_schema_view(
    list=extend_schema(
        summary='Список ремонтов (для авторизованных пользователей)',
        parameters=[
            OpenApiParameter(name='mfn', location='query', type=OpenApiTypes.INT64, required=False, description='узел отказа'),
            OpenApiParameter(name='rec', location='query', type=OpenApiTypes.INT64, required=False, description='способ восстановления'),
        ]
    ),
    retrieve=extend_schema(
        summary='Детальная информация о ремонтах (для авторизованных пользователей)',
    )
)
class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    filter_backends = (django_filters.DjangoFilterBackend, )
    filterset_class = ClaimFilter
    permission_classes = [ClaimPermission, ]
    
    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return ClaimDetailSerializer(*args, **kwargs)
        return ClaimSerializer(*args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == User.CLIENT:
                return Claim.objects.filter(machine__client=user).order_by('failure_date')
            elif user.role == User.SERVICE_COMPANY:
                return Claim.objects.filter(machine__service_company=user).order_by('failure_date')
            else:
                return Claim.objects.all().order_by('failure_date') # для менеджеров
        return Claim.objects.none()
