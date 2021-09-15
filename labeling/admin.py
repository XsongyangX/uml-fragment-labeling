from .models import Label
from django.contrib import admin
from django.utils.html import format_html


# Register your models here.
@admin.register(Label)
class LabelsAdmin(admin.ModelAdmin):
    fields = ("label", "in_english", "validated", )

    # def image(self, obj):
    #     return format_html('<img src="{0}" />'.format(f"/static/fragments/{obj}.png"))