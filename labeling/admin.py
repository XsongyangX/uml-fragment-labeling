from .models import Label
from django.contrib import admin
from django.utils.html import format_html


# Register your models here.
@admin.register(Label)
class LabelsAdmin(admin.ModelAdmin):
    fields = ("label", "in_english", "validated", "display_image")
    readonly_fields = ['display_image']
    
    def display_image(self, obj):
        # get image url 
        image_url = f"/static/fragments/{obj}.png"
        if image_url is not None:
            return format_html('<img src="{}">', image_url)
        return None


    # def image(self, obj):
    #     return format_html('<img src="{0}" />'.format(f"/static/fragments/{obj}.png"))