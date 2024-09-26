from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CLIENT = 'c'
    MANAGER = 'm'
    SERVICE_COMPANY = 's'
    
    ROLE_CHOISES = (
        (CLIENT, 'Клиент'),
        (MANAGER, 'Менеджер'),
        (SERVICE_COMPANY, 'Сервисная компания'),
    )
    
    role = models.CharField(max_length=1, choices=ROLE_CHOISES, default=CLIENT, verbose_name='Роль')
    company_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название компании')
    
    def __str__(self):
        return self.company_name or 'unknown' if self.role in (self.CLIENT, self.SERVICE_COMPANY) else f'{self.last_name} {self.first_name}'
    
