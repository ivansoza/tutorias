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
        self.cargar_alumnos()
        self.cargar_alumnos_mecatronica()
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
                'password': make_password('12345'),  
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

    def cargar_alumnos(self):
        grupo_alumno, _ = Group.objects.get_or_create(name='Alumno')
        posgrado_msc, _ = Posgrado.objects.get_or_create(nombre="Maestría en Sistemas Computacionales")
        alumnos_data = [
            {
                "username": "M23370008",
                "first_name": "Arley Ivan",
                "last_name": "Solis Zacapantzi",
                "apellido_materno": "Zacapantzi",
                "gender": "M",
                "email": "M23370008@apizaco.tecnm.mx"
            },
            {
                "username": "M23370005",
                "first_name": "Miriam",
                "last_name": "Lopez",
                "apellido_materno": "San Luis",
                "gender": "F",
                "email": "M23370005@apizaco.tecnm.mx"
            },
            {
                "username": "M23370004",
                "first_name": "Blanca Estela",
                "last_name": "Islas",
                "apellido_materno": "Flores",
                "gender": "F",
                "email": "M23370004@apizaco.tecnm.mx"
            },
            {
                "username": "M23370001",
                "first_name": "Jorge Alejandro",
                "last_name": "Casco",
                "apellido_materno": "Dominguez",
                "gender": "M",
                "email": "M23370001@apizaco.tecnm.mx"
            },
            {
                "username": "M23370002",
                "first_name": "Jose Ernesto",
                "last_name": "Daza",
                "apellido_materno": "Perez",
                "gender": "M",
                "email": "M23370002@apizaco.tecnm.mx"
            },
            {
                "username": "M23370003",
                "first_name": "Ulises",
                "last_name": "Duran",
                "apellido_materno": "Jimenez",
                "gender": "M",
                "email": "M23370003@apizaco.tecnm.mx"
            },
            {
                "username": "M23370006",
                "first_name": "Enrique",
                "last_name": "Molina",
                "apellido_materno": "Reyes",
                "gender": "H",
                "email": "M23370006@apizaco.tecnm.mx"
            },
            {
                "username": "M23370009",
                "first_name": "Deyanira Yazmin",
                "last_name": "Sanchez",
                "apellido_materno": "Perez",
                "gender": "F",
                "email": "M23370009@apizaco.tecnm.mx"
            },
            {
                "username": "M23370010",
                "first_name": "Bartolome",
                "last_name": "Tellez",
                "apellido_materno": "Chavez",
                "gender": "H",
                "email": "M23370010@apizaco.tecnm.mx"
            },
            {
                "username": "M23370011",
                "first_name": "Eduardo",
                "last_name": "Vazquez",
                "apellido_materno": "Perez",
                "gender": "M",
                "email": "M23370011@apizaco.tecnm.mx"
            },
            {
                "username": "M23370012",
                "first_name": "Itzel",
                "last_name": "Xochitototl",
                "apellido_materno": "Cote",
                "gender": "F",
                "email": "M23370012@apizaco.tecnm.mx"
            },
    
        ]

        # Crear o actualizar los alumnos
        for alumno in alumnos_data:
            user, created = CustomUser.objects.get_or_create(
                username=alumno['username'],
                defaults={
                    'first_name': alumno['first_name'],
                    'last_name': alumno['last_name'],
                    'apellido_materno': alumno['apellido_materno'], 
                    'gender': alumno['gender'],
                    'email': alumno['email'],
                    'password': make_password('12345'),
                    'is_superuser': False,
                    'is_staff': False
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Alumno '{alumno['first_name']}' creado exitosamente."))
                user.groups.add(grupo_alumno)
                user.posgrado_alumno = posgrado_msc
                user.save()
            else:
                self.stdout.write(self.style.WARNING(f"Alumno '{alumno['first_name']}' ya existe. No se realizaron cambios."))


    def cargar_alumnos_mecatronica(self):
        grupo_alumno, _ = Group.objects.get_or_create(name='Alumno')
        posgrado_mec, _ = Posgrado.objects.get_or_create(nombre="Maestría en Ingeniería Mecatrónica")

        # Datos de los alumnos para Maestría en Ingeniería Mecatrónica
        alumnos_data = [
            {
                "username": "M23370054",
                "first_name": "Misael",
                "last_name": "Méndez",
                "apellido_materno": "Cruz",
                "gender": "M",
                "email": "M23370054@apizaco.tecnm.mx"
            },
            {
                "username": "M23370055",
                "first_name": "Juan Carlos",
                "last_name": "Munive",
                "apellido_materno": "Colón",
                "gender": "M",
                "email": "M23370055@apizaco.tecnm.mx"
            },
            {
                "username": "M23370060",
                "first_name": "Xochitl",
                "last_name": "Vasquez",
                "apellido_materno": "Barraza",
                "gender": "F",
                "email": "M23370060@apizaco.tecnm.mx"
            }
            # Añade aquí más alumnos según sea necesario.
        ]

        # Crear o actualizar los alumnos
        for alumno in alumnos_data:
            user, created = CustomUser.objects.get_or_create(
                username=alumno['username'],
                defaults={
                    'first_name': alumno['first_name'],
                    'last_name': alumno['last_name'],
                    'apellido_materno': alumno['apellido_materno'],
                    'gender': alumno['gender'],
                    'email': alumno['email'],
                    'password': make_password('12345'),
                    'is_superuser': False,
                    'is_staff': False
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Alumno '{alumno['first_name']}' creado exitosamente."))
                user.groups.add(grupo_alumno)
                user.posgrado_alumno = posgrado_mec
                user.save()
            else:
                self.stdout.write(self.style.WARNING(f"Alumno '{alumno['first_name']}' ya existe. No se realizaron cambios."))
