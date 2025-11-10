from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Payment)

admin.site.register(models.EMI)

admin.site.register(models.Transaction)