from rest_framework import serializers
from .models import Catalog, Machine, Maintenance, Claim
from accounts.serializers import UserSerializer
from accounts.models import User


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['id', 'category', 'name', 'description']


class MachineSerializer(serializers.ModelSerializer):
    model = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.filter(category=Catalog.TECHNIQUE))
    model_name = serializers.CharField(source='model.name', read_only=True)
    engine_model = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.filter(category=Catalog.ENGINE))
    engine_model_name = serializers.CharField(source='engine_model.name', read_only=True)
    transmission_model = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.filter(category=Catalog.TRANSMISSION))
    transmission_model_name = serializers.CharField(source='transmission_model.name', read_only=True)
    leading_axle_model = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.filter(category=Catalog.LEADING_AXLE))
    leading_axle_model_name = serializers.CharField(source='leading_axle_model.name', read_only=True)
    steerable_axle_model = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.filter(category=Catalog.STEERABLE_AXLE))
    steerable_axle_model_name = serializers.CharField(source='steerable_axle_model.name', read_only=True)
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.CLIENT))
    client_name = serializers.CharField(source='client.company_name', read_only=True)
    service_company = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.SERVICE_COMPANY))
    service_company_name = serializers.CharField(source='service_company.company_name', read_only=True)
    
    class Meta:
        model = Machine
        fields = [
            'id',
            'serial',
            'model',
            'model_name',
            'engine_serial',
            'engine_model',
            'engine_model_name',
            'transmission_serial',
            'transmission_model',
            'transmission_model_name',
            'leading_axle_serial',
            'leading_axle_model',
            'leading_axle_model_name',
            'steerable_axle_serial',
            'steerable_axle_model',
            'steerable_axle_model_name',
            'supply_contract',
            'shipment_date',
            'consumer',
            'delivery_address',
            'equipment',
            'client',
            'client_name',
            'service_company',
            'service_company_name',
        ]
        
        
class MachineDetailSerializer(serializers.ModelSerializer):
    model = CatalogSerializer(read_only=True)
    engine_model = CatalogSerializer(read_only=True)
    transmission_model = CatalogSerializer(read_only=True)
    leading_axle_model = CatalogSerializer(read_only=True)
    steerable_axle_model = CatalogSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    service_company = UserSerializer(read_only=True)
    
    class Meta:
        model = Machine
        fields = [
            'id', 
            'serial', 
            'model',
            'engine_serial',
            'engine_model',
            'transmission_serial',
            'transmission_model',
            'leading_axle_serial',
            'leading_axle_model',
            'steerable_axle_serial',
            'steerable_axle_model',
            'supply_contract',
            'shipment_date',
            'consumer',
            'delivery_address',
            'equipment',
            'client',    
            'service_company',        
        ]


class MaintenanceSerializer(serializers.ModelSerializer):
    maintenance_date = serializers.DateField(format='%d.%m.%Y')
    order_date = serializers.DateField(format='%d.%m.%Y')
    machine_serial = serializers.CharField(source='machine.serial', read_only=True)
    machine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())
    maintenance_type_name = serializers.CharField(source='maintenance_type.name', read_only=True)
    maintenance_type = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.filter(category=Catalog.MAINTENANCE))
    service_company_name = serializers.CharField(source='service_company.company_name', read_only=True)
    service_company = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.filter(role=User.SERVICE_COMPANY))
    
    class Meta:
        model = Maintenance
        fields = [
            'id',
            'maintenance_date',
            'engine_hours',
            'order_number',
            'order_date',
            'machine_serial',
            'machine',
            'maintenance_type_name',
            'maintenance_type',
            'service_company_name',
            'service_company',
        ]


class MaintenanceDetailSerializer(serializers.ModelSerializer):
    machine_serial = serializers.CharField(source='machine.serial', read_only=True)
    machine_model = serializers.CharField(source='machine.model.name', read_only=True)
    machine_description = serializers.CharField(source='machine.model.description', read_only=True)
    maintenance_type = CatalogSerializer(read_only=True)
    service_company = UserSerializer(read_only=True)
    
    class Meta:
        model = Maintenance
        fields = [
            'id',
            'maintenance_date',
            'engine_hours',
            'order_number',
            'order_date',
            'machine_serial',
            'machine_model',
            'machine_description',
            'maintenance_type',
            'service_company',
        ]


class ClaimSerializer(serializers.ModelSerializer):
    machine_serial = serializers.CharField(source='machine.serial', read_only=True)
    machine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())
    malfunction_node_name = serializers.CharField(source='malfunction_node.name', read_only=True)
    malfunction_node = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.filter(category=Catalog.MALFUNCTION_NODE))
    recovery_method_name = serializers.CharField(source='recovery_method.name', read_only=True)
    recovery_method = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.filter(category=Catalog.RECOVERY_METHOD))
    service_company_name = serializers.CharField(source='service_company.company_name', read_only=True)
    service_company = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.filter(role=User.SERVICE_COMPANY))
    downtime = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Claim
        fields = [
            'id',
            'failure_date',
            'engine_hours',
            'failure_description',
            'restoration_date',
            'downtime',
            'machine_serial',
            'machine',
            'malfunction_node_name',
            'malfunction_node',
            'recovery_method_name',
            'recovery_method',
            'service_company_name',
            'service_company',
            'spare_parts',
        ]


class ClaimDetailSerializer(serializers.ModelSerializer):
    machine_serial = serializers.CharField(source='machine.serial', read_only=True)
    machine_model = serializers.CharField(source='machine.model.name', read_only=True)
    machine_description = serializers.CharField(source='machine.model.description', read_only=True)
    malfunction_node = CatalogSerializer(read_only=True)
    recovery_method = CatalogSerializer(read_only=True)
    service_company = UserSerializer(read_only=True)
    
    class Meta:
        model = Claim
        fields = [
            'id',
            'failure_date',
            'engine_hours',
            'failure_description',
            'restoration_date',
            'downtime',
            'machine_serial',
            'machine_model',
            'machine_description',
            'malfunction_node',
            'recovery_method',
            'service_company',
            'spare_parts',
        ]