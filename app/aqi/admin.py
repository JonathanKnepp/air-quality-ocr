from django.contrib import admin
from .models import AQIEntry


class AQIEntryAdmin(admin.ModelAdmin):
    ordering = ('capture_time', )
    list_display = ['temperature', 'humidity', 'tvoc', 'hcho', 'pm2_5', 'pm10', 'co2', 'capture_time', 'created']

admin.site.register(AQIEntry, AQIEntryAdmin)
