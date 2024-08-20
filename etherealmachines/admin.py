from django.contrib import admin
from .models import EtherealMachine, AxisData


@admin.register(EtherealMachine)
class EtherealMachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'feedrate', 'max_acceleration', 'max_velocity', 'acceleration', 'angular_units', 'velocity', 'timestamp')

@admin.register(AxisData)
class AxisDataAdmin(admin.ModelAdmin):
    list_display = ('machine', 'axis', 'actual_position', 'distance_to_go', 'tool_offset', 'homed')
