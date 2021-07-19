from .models import Label
from django.contrib import admin

# Register your models here.
@admin.register(Label)
class LabelsAdmin(admin.ModelAdmin):
    fields = ("label", )