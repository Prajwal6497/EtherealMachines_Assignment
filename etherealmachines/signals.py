from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import EtherealMachine, AxisData

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    manager_group, created = Group.objects.get_or_create(name='Manager')
    supervisor_group, created = Group.objects.get_or_create(name='Supervisor')
    operator_group, created = Group.objects.get_or_create(name='Operator')

    machine_ct = ContentType.objects.get_for_model(EtherealMachine)
    axisdata_ct = ContentType.objects.get_for_model(AxisData)

    manager_permissions = [
        Permission.objects.get(codename='add_machine'),
        Permission.objects.get(codename='view_machine'),
        Permission.objects.get(codename='change_machine'),
    ]
    manager_group.permissions.set(manager_permissions)

    supervisor_permissions = [
        Permission.objects.get(codename='view_machine'),
        Permission.objects.get(codename='change_machine'),
    ]
    supervisor_group.permissions.set(supervisor_permissions)

    operator_permissions = [
        Permission.objects.get(codename='view_machine'),
    ]
    operator_group.permissions.set(operator_permissions)
