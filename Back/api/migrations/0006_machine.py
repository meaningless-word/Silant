# Generated by Django 5.1.1 on 2024-09-11 16:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_delete_machine'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=100, unique=True, verbose_name='Зав. номер')),
                ('engine_serial', models.CharField(max_length=100, verbose_name='Зав. номер двигателя')),
                ('transmission_serial', models.CharField(max_length=100, verbose_name='Зав. номер трансмиссии')),
                ('leading_axle_serial', models.CharField(max_length=100, verbose_name='Зав. номер ведущего моста')),
                ('steerable_axle_serial', models.CharField(max_length=100, verbose_name='Зав. номер управляемого моста')),
                ('supply_contract', models.CharField(max_length=100, verbose_name='Договор поставки №, дата')),
                ('shipment_date', models.DateField(verbose_name='Дата отгрузки')),
                ('consumer', models.CharField(max_length=100, verbose_name='Грузополучатель (конечный потребитель)')),
                ('delivery_address', models.CharField(max_length=255, verbose_name='Адрес поставки')),
                ('equipment', models.TextField(verbose_name='Комплектация')),
                ('client', models.ForeignKey(limit_choices_to={'role': 'c'}, on_delete=django.db.models.deletion.RESTRICT, related_name='machines', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('engine_model', models.ForeignKey(limit_choices_to={'category': 'eng'}, on_delete=django.db.models.deletion.RESTRICT, related_name='engine_models', to='api.catalogue', verbose_name='Модель двигателя')),
                ('leading_axle_model', models.ForeignKey(limit_choices_to={'category': 'lda'}, on_delete=django.db.models.deletion.RESTRICT, related_name='leading_axle_models', to='api.catalogue', verbose_name='Модель ведущего моста')),
                ('model', models.ForeignKey(limit_choices_to={'category': 'tec'}, on_delete=django.db.models.deletion.RESTRICT, related_name='machine_models', to='api.catalogue', verbose_name='Модель техники')),
                ('service_company', models.ForeignKey(limit_choices_to={'category': 'sco'}, on_delete=django.db.models.deletion.RESTRICT, related_name='service_companies', to='api.catalogue', verbose_name='Сервисная компания')),
                ('steerable_axle_model', models.ForeignKey(limit_choices_to={'category': 'sta'}, on_delete=django.db.models.deletion.RESTRICT, related_name='steerable_axle_models', to='api.catalogue', verbose_name='Модель управляемого моста')),
                ('transmission_model', models.ForeignKey(limit_choices_to={'category': 'trm'}, on_delete=django.db.models.deletion.RESTRICT, related_name='transmission_models', to='api.catalogue', verbose_name='Модель трансмиссии')),
            ],
            options={
                'verbose_name': 'Машина',
                'verbose_name_plural': 'Машины',
            },
        ),
    ]
