from django.contrib import admin
from .models import *

# Register your models here.x
@admin.register(Post)
class Admin(admin.ModelAdmin):
    class Meta:
        fieldsets = (
            (None, {
                "fields": (
                    '__all__'
                ),
            }),
        )
        
@admin.register(Like)
class Admin(admin.ModelAdmin):
    class meta:
        pass
