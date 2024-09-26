from django.contrib import admin
from .models import (Catalog, Machine, Maintenance, Claim)

admin.site.register(Catalog)
admin.site.register(Machine)
admin.site.register(Maintenance)
admin.site.register(Claim)
