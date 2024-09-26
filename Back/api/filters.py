import django_filters
from .models import Machine, Maintenance, Claim


class MachineFilter(django_filters.FilterSet):
    serial = django_filters.CharFilter(field_name='serial',lookup_expr='iexact')
    tec = django_filters.NumberFilter(field_name='model',lookup_expr='exact')
    eng = django_filters.NumberFilter(field_name='engine_model',lookup_expr='exact')
    trm = django_filters.NumberFilter(field_name='transmission_model',lookup_expr='exact')
    lda = django_filters.NumberFilter(field_name='leading_axle_model',lookup_expr='exact')
    sta = django_filters.NumberFilter(field_name='steerable_axle_model',lookup_expr='exact')
    
    class Meta:
        model = Machine
        fields = [
            'serial',
            'tec',
            'eng',
            'trm',
            'lda',
            'sta',
        ]


class MaintenanceFilter(django_filters.FilterSet):
    serial = django_filters.CharFilter(field_name='machine__serial',lookup_expr='iexact')
    s = django_filters.NumberFilter(field_name='service_company',lookup_expr='exact')
    man = django_filters.NumberFilter(field_name='maintenance_type__id',lookup_expr='exact')
    
    class Meta:
        model = Maintenance
        fields = [
            'serial',
            'man',
            's',
        ]


class ClaimFilter(django_filters.FilterSet):
    mfn = django_filters.NumberFilter(field_name='malfunction_node__id',lookup_expr='exact')
    rec = django_filters.NumberFilter(field_name='recovery_method__id',lookup_expr='exact')
    
    class Meta:
        model = Claim
        fields = [
            'mfn',
            'rec',
        ]