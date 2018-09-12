from django.contrib import admin
from ifrs.models import Transaction
from ifrs.models import Setting

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Setting)
