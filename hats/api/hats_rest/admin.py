from django.contrib import admin
from hats_rest.models import Hat

# Register your models here.
@admin.register(Hat)
class HatAdmin(admin.ModelAdmin):
    pass
