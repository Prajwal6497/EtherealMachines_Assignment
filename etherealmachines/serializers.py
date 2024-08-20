from rest_framework import serializers
from .models import EtherealMachine, AxisData

class AxisDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxisData
        fields = ['axis', 'actual_position', 'distance_to_go', 'tool_offset', 'homed']

class MachineSerializer(serializers.ModelSerializer):
    actual_position = serializers.SerializerMethodField()
    tool_offset = serializers.SerializerMethodField()
    distance_to_go = serializers.SerializerMethodField()
    homed = serializers.SerializerMethodField()

    class Meta:
        model = EtherealMachine
        fields = [
            'name', 'feedrate', 'max_acceleration', 'max_velocity',
            'acceleration', 'angular_units', 'velocity', 'timestamp',
            'actual_position', 'tool_offset', 'distance_to_go', 'homed'
        ]

    def get_actual_position(self, obj):
        axis_data = obj.axis_data.all()
        position = {axis.lower(): 0.0 for axis in ['X', 'Y', 'Z', 'A', 'C']}
        for data in axis_data:
            if data.axis in ['X', 'Y', 'Z', 'A', 'C']:
                position[data.axis.lower()] = data.actual_position
        return position

    def get_tool_offset(self, obj):
        axis_data = obj.axis_data.all()
        offsets = {axis.lower(): 0.0 for axis in ['X', 'Y', 'Z', 'A', 'C']}
        for data in axis_data:
            if data.axis in ['X', 'Y', 'Z', 'A', 'C']:
                offsets[data.axis.lower()] = data.tool_offset
        return offsets

    def get_distance_to_go(self, obj):
        axis_data = obj.axis_data.all()
        distances = {axis.lower(): 0.0 for axis in ['X', 'Y', 'Z', 'A', 'C']}
        for data in axis_data:
            if data.axis in ['X', 'Y', 'Z', 'A', 'C']:
                distances[data.axis.lower()] = data.distance_to_go
        return distances

    def get_homed(self, obj):
        axis_data = obj.axis_data.all()
        homed_status = {axis.lower(): False for axis in ['X', 'Y', 'Z', 'A', 'C']}
        for data in axis_data:
            if data.axis in ['X', 'Y', 'Z', 'A', 'C']:
                homed_status[data.axis.lower()] = data.homed
        return homed_status

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Rename fields and format numbers
        representation['Name'] = representation.pop('name')
        representation['Feedrate'] = format(float(representation.pop('feedrate')), '.1f')
        representation['Max_acceleration'] = format(float(representation.pop('max_acceleration')), '.4f')
        representation['Max_velocity'] = format(float(representation.pop('max_velocity')), '.4f')
        representation['Acceleration'] = format(float(representation.pop('acceleration')), '.1f')
        representation['Angular_units'] = format(float(representation.pop('angular_units')), '.4f')
        representation['Velocity'] = format(float(representation.pop('velocity')), '.1f')
        # Format timestamp
        timestamp = representation.pop('timestamp')
        representation['Timestamp'] = timestamp.replace('T', ' ').split('.')[0]
        return representation
