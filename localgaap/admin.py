from django.contrib import admin
from localgaap.models import Transaction
from localgaap.models import Setting

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Setting)
