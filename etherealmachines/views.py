
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .models import EtherealMachine, AxisData
from .serializers import MachineSerializer, AxisDataSerializer
from django.contrib.auth.models import User, Group
from rest_framework.permissions import BasePermission
import threading
import time
from django.utils import timezone

# Custom Permissions
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Supervisor').exists()

class IsOperator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Operator').exists()

# Machine ViewSet
class MachineViewSet(viewsets.ModelViewSet):
    queryset = EtherealMachine.objects.all()
    serializer_class = MachineSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated & IsManager]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated & (IsManager | IsSupervisor)]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated & IsManager]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(MachineViewSet, self).get_permissions()

    @action(detail=True, methods=['get'])
    def machine_details(self, request, pk=None):
        machine = get_object_or_404(EtherealMachine, pk=pk)
        serializer = self.get_serializer(machine)
        print(serializer.data)
        return Response(serializer.data)


# Function to read from Cnc.txt and update the database
def read_cnc_file():
    while True:
        try:
            with open('Cnc.txt', 'r') as file:
                lines = file.readlines()

                machine_name = None
                acceleration = None
                actual_positions = []
                distances_to_go = []
                homed_statuses = []
                tool_offsets = []
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('Name'):
                        if machine_name:
                            save_machine_data(
                                machine_name, acceleration, actual_positions,
                                distances_to_go, homed_statuses, tool_offsets
                            )

                        machine_name = line.split()[1]
                        acceleration = None
                        actual_positions = []
                        distances_to_go = []
                        homed_statuses = []
                        tool_offsets = []

                    elif line.startswith('acceleration'):
                        acceleration = float(line.split()[1].replace(',', '.'))
                    elif line.startswith('actual_position'):
                        actual_positions = [float(pos.replace(',', '.')) for pos in line.split()[1:]]
                    elif line.startswith('distance_to_go'):
                        distances_to_go = [float(dist.replace(',', '.')) for dist in line.split()[1:]]
                    elif line.startswith('homed'):
                        homed_statuses = [bool(int(h)) for h in line.split()[1:]]
                    elif line.startswith('tool_offset'):
                        tool_offsets = [float(offset.replace(',', '.')) for offset in line.split()[1:]]
                    elif line.startswith('velocity'):
                        pass

                if machine_name:
                    save_machine_data(
                        machine_name, acceleration, actual_positions,
                        distances_to_go, homed_statuses, tool_offsets
                    )
            time.sleep(0.5)
        except Exception as e:
            print(f"Error reading from file: {e}")
            time.sleep(0.5)

# Start the file reading in a separate thread
file_reading_thread = threading.Thread(target=read_cnc_file, daemon=True)
file_reading_thread.start()


def save_machine_data(machine_name, acceleration, actual_positions, distances_to_go, homed_statuses, tool_offsets):
    machine, _ = EtherealMachine.objects.update_or_create(
        name=machine_name,
        defaults={
            'acceleration': acceleration,
            'feedrate': 1.0,
            'max_acceleration': 20.0000,
            'max_velocity': 1.2000,
            'angular_units': 1.0000,
            'velocity': 30.0,
            'timestamp': timezone.now()
        }
    )

    axis_order = ['X', 'Y', 'Z', 'A', 'C']
    
    for i, axis in enumerate(axis_order):
        if i < len(actual_positions):
            AxisData.objects.update_or_create(
                machine=machine,
                axis=axis,
                defaults={
                    'actual_position': actual_positions[i],
                    'distance_to_go': distances_to_go[i],
                    'tool_offset': tool_offsets[i] if i < len(tool_offsets) else 0.0,
                    'homed': homed_statuses[i] if i < len(homed_statuses) else False
                }
            )
