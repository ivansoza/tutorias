from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from generales.models import Posgrado  # Asegúrate de importar tu modelo Posgrado correctamente
from django.contrib.auth.hashers import make_password
from usuarios.models import CustomUser
from django.core.management import call_command  # Importar call_command para ejecutar otros comandos de administración

class Command(BaseCommand):
    help = 'Crea los grupos y posgrados iniciales si no existen'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando la carga de datos...")
        self.stdout.write(self.style.WARNING('Aplicando migraciones...'))
        call_command('makemigrations')
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Migraciones completadas.'))

        # Llamar a la función para cargar los grupos
        self.cargar_grupos()

        # Llamar a la función para cargar los posgrados
        self.cargar_posgrados()
        self.cargar_usuario_admin()

        self.stdout.write(self.style.SUCCESS('Carga de datos completada.'))

    def cargar_grupos(self):
        """
        Función para cargar los grupos
        """
        grupos = ['Coordinador', 'Docente', 'Alumno']

        for nombre_grupo in grupos:
            group, created = Group.objects.get_or_create(name=nombre_grupo)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{nombre_grupo}" creado con éxito.'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo "{nombre_grupo}" ya existe.'))

        self.stdout.write(self.style.SUCCESS('Proceso de creación de grupos completado.'))

    def cargar_posgrados(self):
        """
        Función para cargar los posgrados
        """
        posgrados_names = [
            "Maestría en Sistemas Computacionales",
            "Maestría en Ingeniería Mecatrónica",
            "Maestría en Ingeniería Administrativa",
            "Doctorado en Ciencias de la Ingeniería"
        ]

        for name in posgrados_names:
            posgrado, created = Posgrado.objects.get_or_create(nombre=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Posgrado "{name}" creado con éxito.'))
            else:
                self.stdout.write(self.style.WARNING(f'Posgrado "{name}" ya existe.'))

        self.stdout.write(self.style.SUCCESS('Proceso de creación de posgrados completado.'))
    def cargar_usuario_admin(self):
        """
        Función para crear un superusuario con los detalles específicos.
        """
        admin_user, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'password': make_password('12345'),  # Contraseña del 1 al 5
                'first_name': 'Miriam',
                'last_name': 'Lopez',
                'apellido_materno': 'Sanluis',
                'email': 'm23370005@apizaco.tecnm.mx',
                'is_superuser': True,
                'is_staff': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Usuario 'admin' creado exitosamente como superusuario."))
        else:
            self.stdout.write(self.style.WARNING("Usuario 'admin' ya existe. Actualizando los datos..."))
            admin_user.email = 'm23370005@apizaco.tecnm.mx'
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.first_name = 'Miriam'
            admin_user.last_name = 'Lopez'
            admin_user.apellido_materno = 'Sanluis'
            admin_user.password = make_password('12345')  # Actualizar la contraseña
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Usuario 'admin' actualizado exitosamente."))