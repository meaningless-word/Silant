from django.db import models
from accounts.models import User


class Catalog(models.Model):
    TECHNIQUE = 'tec'
    ENGINE = 'eng'
    TRANSMISSION = 'trm'
    LEADING_AXLE = 'lda'
    STEERABLE_AXLE = 'sta'
    MAINTENANCE = 'man'
    MALFUNCTION_NODE ='mfn'
    RECOVERY_METHOD = 'rec'
    CATEGORY_CHOISES = (
        (TECHNIQUE, 'Модель техники'),
        (ENGINE, 'Модель двигателя'),
        (TRANSMISSION, 'Модель трансмиссии'),
        (LEADING_AXLE, 'Модель ведущего моста'),
        (STEERABLE_AXLE, 'Модель управляемого моста'),
        (MAINTENANCE, 'Вид ТО'),
        (MALFUNCTION_NODE, 'Узел отказа'),
        (RECOVERY_METHOD, 'Способ восстановления'),
    )
    
    category = models.CharField(max_length=3, choices=CATEGORY_CHOISES, verbose_name='Категория')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'
        
    def __str__(self):
        return f'{self.name} ({self.category})'


class Machine(models.Model):
    serial = models.CharField(max_length=100, unique=True, verbose_name='Зав. номер')
    model = models.ForeignKey(Catalog, on_delete=models.RESTRICT, related_name='machine_models', limit_choices_to={'category': Catalog.TECHNIQUE}, verbose_name='Модель техники')
    engine_model = models.ForeignKey(Catalog, on_delete=models.RESTRICT, related_name='engine_models', limit_choices_to={'category': Catalog.ENGINE}, verbose_name='Модель двигателя') 
    engine_serial = models.CharField(max_length=100,verbose_name='Зав. номер двигателя')
    transmission_model = models.ForeignKey(Catalog, on_delete=models.RESTRICT, related_name='transmission_models', limit_choices_to={'category': Catalog.TRANSMISSION}, verbose_name='Модель трансмиссии')
    transmission_serial = models.CharField(max_length=100, verbose_name='Зав. номер трансмиссии')
    leading_axle_model = models.ForeignKey(Catalog, on_delete=models.RESTRICT, related_name='leading_axle_models', limit_choices_to={'category': Catalog.LEADING_AXLE}, verbose_name='Модель ведущего моста')
    leading_axle_serial = models.CharField(max_length=100, verbose_name='Зав. номер ведущего моста')
    steerable_axle_model = models.ForeignKey(Catalog, on_delete=models.RESTRICT, related_name='steerable_axle_models', limit_choices_to={'category': Catalog.STEERABLE_AXLE}, verbose_name='Модель управляемого моста')
    steerable_axle_serial = models.CharField(max_length=100, verbose_name='Зав. номер управляемого моста')
    supply_contract = models.CharField(max_length=100, verbose_name='Договор поставки №, дата')
    shipment_date = models.DateField(verbose_name='Дата отгрузки')
    consumer = models.CharField(max_length=100, verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес поставки')
    equipment = models.TextField(verbose_name='Комплектация')
    client = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='machines',limit_choices_to={'role': User.CLIENT}, verbose_name='Клиент')
    service_company = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='serviced_machines', limit_choices_to={'role': User.SERVICE_COMPANY}, verbose_name='Сервисная компания')
    
    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины' 
        
    def __str__(self):
        return f'{self.model} {self.serial}'


class Maintenance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.RESTRICT, related_name='maintenances', verbose_name='Машина')
    maintenance_type = models.ForeignKey(Catalog, on_delete=models.RESTRICT, related_name='maintenance_types', limit_choices_to={'category': Catalog.MAINTENANCE}, verbose_name='Вид ТО')
    maintenance_date = models.DateField(verbose_name='Дата проведения ТО')
    engine_hours = models.IntegerField(default=0, verbose_name='Наработка, м/час')
    order_number = models.CharField(max_length=100, verbose_name='№ заказ-наряда')
    order_date = models.DateField(verbose_name='Дата заказа-наряда')
    service_company = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='maintenances', limit_choices_to={'role': User.SERVICE_COMPANY}, null=True, blank=True, verbose_name='Сервисная компания')
    
    class Meta:
        verbose_name = 'ТО'
        verbose_name_plural = 'ТО'
        
    def __str__(self):
        return f'{self.machine}/[{self.maintenance_type}]/{self.service_company if self.service_company else 'самостоятельно'}'


class Claim(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.RESTRICT, related_name='claims', verbose_name='Машина')
    failure_date = models.DateField(verbose_name='Дата отказа')
    engine_hours = models.IntegerField(default=0, verbose_name='Наработка, м/час')
    malfunction_node = models.ForeignKey(Catalog, on_delete=models.RESTRICT, related_name='malfunction_nodes', limit_choices_to={'category': Catalog.MALFUNCTION_NODE}, verbose_name='Узел отказа')
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.ForeignKey(Catalog, on_delete=models.RESTRICT, related_name='recovery_methods', limit_choices_to={'category': Catalog.RECOVERY_METHOD}, verbose_name='Метод восстановления')
    spare_parts = models.TextField(default="", null=True, blank=True, verbose_name='Запасные части')
    restoration_date = models.DateField(blank=True, null=True, verbose_name='Дата восстановления')
    downtime = models.IntegerField(editable=False, verbose_name='Время простоя техники')
    service_company = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='claims', limit_choices_to={'role': User.SERVICE_COMPANY}, null=True, blank=True, verbose_name='Сервисная компания')
    
    class Meta:
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'
    
    def save(self, *args, **kwargs):
        if self.restoration_date and self.failure_date:
            self.downtime = (self.restoration_date - self.failure_date).days
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.machine} {self.service_company if self.service_company else 'самостоятельно'}'
