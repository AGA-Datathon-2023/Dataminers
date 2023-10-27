from django.contrib import admin
from .models import Transaction

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("None", {"fields": ["datetime", "method", "path", "status_code", ]}),
    ]
    
    list_display = ["datetime", "method", "path", "status_code", ]


admin.site.register(Transaction, TransactionAdmin)