"""
Management command to seed initial data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import date

from units.models import UnitTower, UnitBlock, Unit, UnitMembership
from amenities.models import Amenity
from maintenance.models import Supplier

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed initial data for the application'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial data...')
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@condominio.com',
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'is_staff': True,
                'is_superuser': True,
                'is_resident': False
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            # Assign to Admin group
            admin_group = Group.objects.get(name='Admin')
            admin_user.groups.add(admin_group)
            self.stdout.write(f'Created admin user: {admin_user.username}')
        
        # Create sample resident user
        resident_user, created = User.objects.get_or_create(
            username='jperez',
            defaults={
                'email': 'jperez@email.com',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'document_number': '12345678-9',
                'phone': '+56912345678',
                'is_resident': True
            }
        )
        if created:
            resident_user.set_password('resident123')
            resident_user.save()
            self.stdout.write(f'Created resident user: {resident_user.username}')
        
        # Create sample towers
        torre_a, _ = UnitTower.objects.get_or_create(
            name='Torre A',
            defaults={'description': 'Torre principal del condominio'}
        )
        
        torre_b, _ = UnitTower.objects.get_or_create(
            name='Torre B',
            defaults={'description': 'Torre secundaria del condominio'}
        )
        
        # Create sample blocks
        bloque_1a, _ = UnitBlock.objects.get_or_create(
            tower=torre_a,
            name='Bloque 1',
            defaults={'description': 'Primer bloque de Torre A'}
        )
        
        bloque_2a, _ = UnitBlock.objects.get_or_create(
            tower=torre_a,
            name='Bloque 2',
            defaults={'description': 'Segundo bloque de Torre A'}
        )
        
        # Create sample units
        units_data = [
            {'block': bloque_1a, 'code': 'A1-101', 'category': 'departamento', 'floor': 1, 'number': '101', 'status': 'propietario'},
            {'block': bloque_1a, 'code': 'A1-102', 'category': 'departamento', 'floor': 1, 'number': '102', 'status': 'vacio'},
            {'block': bloque_1a, 'code': 'A1-201', 'category': 'departamento', 'floor': 2, 'number': '201', 'status': 'inquilino'},
            {'block': bloque_1a, 'code': 'A1-C01', 'category': 'cochera', 'floor': 0, 'number': 'C01', 'status': 'propietario'},
            {'block': bloque_2a, 'code': 'A2-101', 'category': 'departamento', 'floor': 1, 'number': '101', 'status': 'vacio'},
        ]
        
        for unit_data in units_data:
            unit, created = Unit.objects.get_or_create(
                code=unit_data['code'],
                defaults=unit_data
            )
            if created:
                self.stdout.write(f'Created unit: {unit.code}')
        
        # Assign resident to a unit
        unit_a1_101 = Unit.objects.get(code='A1-101')
        unit_a1_101.owner = resident_user
        unit_a1_101.save()
        
        # Create unit membership
        UnitMembership.objects.get_or_create(
            unit=unit_a1_101,
            user=resident_user,
            defaults={
                'role_in_unit': 'propietario',
                'start_date': date.today()
            }
        )
        
        # Create sample amenities
        amenities_data = [
            {
                'name': 'Piscina',
                'amenity_type': 'pool',
                'description': 'Piscina comunitaria con área de descanso',
                'capacity': 20,
                'location': 'Área exterior'
            },
            {
                'name': 'Quincho',
                'amenity_type': 'bbq',
                'description': 'Área de parrillas y eventos',
                'capacity': 30,
                'location': 'Área de eventos'
            },
            {
                'name': 'Gimnasio',
                'amenity_type': 'gym',
                'description': 'Gimnasio equipado con máquinas básicas',
                'capacity': 10,
                'location': 'Primer piso'
            }
        ]
        
        for amenity_data in amenities_data:
            amenity, created = Amenity.objects.get_or_create(
                name=amenity_data['name'],
                defaults=amenity_data
            )
            if created:
                self.stdout.write(f'Created amenity: {amenity.name}')
        
        # Create sample suppliers
        suppliers_data = [
            {
                'name': 'Servicios Técnicos Ltda.',
                'contact_person': 'Carlos Mendoza',
                'phone': '+56987654321',
                'email': 'contacto@serviciotecnico.cl'
            },
            {
                'name': 'Mantención Integral',
                'contact_person': 'Ana García',
                'phone': '+56976543210',
                'email': 'ana@mantencion.cl'
            }
        ]
        
        for supplier_data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                name=supplier_data['name'],
                defaults=supplier_data
            )
            if created:
                self.stdout.write(f'Created supplier: {supplier.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded initial data!')
        )