from django.db import models

# model to store general machine details
class EtherealMachine(models.Model):
    name = models.CharField(max_length=100)
    feedrate = models.FloatField()
    max_acceleration = models.FloatField()
    max_velocity = models.FloatField()
    acceleration = models.FloatField()
    angular_units = models.FloatField()
    velocity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

# model to store information about each axis for the machine.
class AxisData(models.Model):
    machine = models.ForeignKey(EtherealMachine, related_name='axis_data', on_delete=models.CASCADE)
    axis = models.CharField(max_length=1)  # X, Y, Z, A, C 
    actual_position = models.FloatField()
    distance_to_go = models.FloatField()
    tool_offset = models.FloatField()
    homed = models.BooleanField(default=False)
