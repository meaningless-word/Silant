# Generated by Django 5.1.1 on 2024-09-19 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_catalog_category_alter_claim_service_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='spare_parts',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Запасные части'),
        ),
    ]
