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
        self.cargar_docentes_software()

        self.cargar_docentes_administracion()

        self.cargar_docentes_mecatronica()
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

        


    def cargar_docentes_software(self):
        grupo_docente, _ = Group.objects.get_or_create(name='Docente')
        posgrado_msc, _ = Posgrado.objects.get_or_create(nombre="Maestría en Sistemas Computacionales")

        # Datos de los docentes para Maestría en Sistemas Computacionales
        docentes_data = [
                {
                    "username": "juan.rr",
                    "first_name": "Juan",
                    "last_name": "Ramos",
                    "apellido_materno": "Ramos",
                    "gender": "M",
                    "email": "juan.rr@apizaco.tecnm.mx"
                },
                {
                    "username": "janai.sh",
                    "first_name": "María Janai",
                    "last_name": "Sánchez",
                    "apellido_materno": "Hernández",
                    "gender": "F",
                    "email": "janai.sh@apizaco.tecnm.mx"
                },
                {
                    "username": "elizabeth.cc",
                    "first_name": "Elizabeth",
                    "last_name": "Cuatecontzi",
                    "apellido_materno": "Cuahutle",
                    "gender": "F",
                    "email": "elizabeth.cc@apizaco.tecnm.mx"
                },
                {
                    "username": "juan.hm",
                    "first_name": "José Juan",
                    "last_name": "Hernández",
                    "apellido_materno": "Mora",
                    "gender": "M",
                    "email": "juan.hm@apizaco.tecnm.mx"
                },
                {
                    "username": "guadalupe.mb",
                    "first_name": "María Guadalupe",
                    "last_name": "Medina",
                    "apellido_materno": "Barrera",
                    "gender": "F",
                    "email": "guadalupe.mb@apizaco.tecnm.mx"
                },
                {
                    "username": "eduardo.sl",
                    "first_name": "Eduardo",
                    "last_name": "Sánchez",
                    "apellido_materno": "Lucero",
                    "gender": "M",
                    "email": "eduardo.sl@apizaco.tecnm.mx"
                },
                {
                    "username": "edmundo.bh",
                    "first_name": "Edmundo",
                    "last_name": "Bonilla",
                    "apellido_materno": "Huerta",
                    "gender": "M",
                    "email": "edmundo.bh@apizaco.tecnm.mx"
                },
                {
                    "username": "yesenia.gm",
                    "first_name": "Yesenia Nohemí",
                    "last_name": "González",
                    "apellido_materno": "Meneses",
                    "gender": "F",
                    "email": "yesenia.gm@apizaco.tecnm.mx"
                },
                {
                    "username": "blanca.pm",
                    "first_name": "Blanca Estela",
                    "last_name": "Pedroza",
                    "apellido_materno": "Méndez",
                    "gender": "F",
                    "email": "blanca.pm@apizaco.tecnm.mx"
                },
                {
                    "username": "rodolfo.pl",
                    "first_name": "Rodolfo Eleazar",
                    "last_name": "Pérez",
                    "apellido_materno": "Loaiza",
                    "gender": "M",
                    "email": "rodolfo.pl@apizaco.tecnm.mx"
                },
                {
                    "username": "federico.rc",
                    "first_name": "José Federico",
                    "last_name": "Ramírez",
                    "apellido_materno": "Cruz",
                    "gender": "M",
                    "email": "federico.rc@apizaco.tecnm.mx"
                },
                {
                    "username": "crispin.hh",
                    "first_name": "José Crispín",
                    "last_name": "Hernández",
                    "apellido_materno": "Hernández",
                    "gender": "M",
                    "email": "crispin.hh@apizaco.tecnm.mx"
                },
                {
                    "username": "perfecto.qf",
                    "first_name": "Perfecto Malaquías",
                    "last_name": "Quintero",
                    "apellido_materno": "Flores",
                    "gender": "M",
                    "email": "perfecto.qf@apizaco.tecnm.mx"
                },
                {
                    "username": "higinio.nb",
                    "first_name": "Higinio",
                    "last_name": "Nava",
                    "apellido_materno": "Bautista",
                    "gender": "M",
                    "email": "higinio.nb@apizaco.tecnm.mx"
                },
                {
                    "username": "carlos.pc",
                    "first_name": "Carlos",
                    "last_name": "Pérez",
                    "apellido_materno": "Corona",
                    "gender": "M",
                    "email": "carlos.pc@apizaco.tecnm.mx"
                }
        ]

        # Crear o actualizar los docentes
        for docente in docentes_data:
            user, created = CustomUser.objects.get_or_create(
                username=docente['username'],
                defaults={
                    'first_name': docente['first_name'],
                    'last_name': docente['last_name'],
                    'apellido_materno': docente['apellido_materno'],
                    'gender': docente['gender'],
                    'email': docente['email'],
                    'password': make_password('12345'),
                    'is_superuser': False,
                    'is_staff': True  # Considerando que son docentes, podrías querer marcarlos como staff
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Docente '{docente['first_name']}' creado exitosamente."))
                user.groups.add(grupo_docente)
                user.posgrado_docente.add(posgrado_msc)  # Asumiendo que posgrado_docente es un ManyToManyField
                user.save()
            else:
                self.stdout.write(self.style.WARNING(f"Docente '{docente['first_name']}' ya existe. No se realizaron cambios."))



    def cargar_docentes_administracion(self):
        grupo_docente, _ = Group.objects.get_or_create(name='Docente')
        posgrado_admin, _ = Posgrado.objects.get_or_create(nombre="Maestría en Ingeniería Administrativa")

        # Datos de los docentes para Maestría en Ingeniería Administrativa
        docentes_data = [
            {
                "username": "miguel.rl",
                "first_name": "Miguel Ángel",
                "last_name": "Rodríguez",
                "apellido_materno": "Lozada",
                "gender": "M",
                "email": "miguel.rl@apizaco.tecnm.mx"
            },
            {
                "username": "kathy.vm",
                "first_name": "Kathy Laura",
                "last_name": "Vargas",
                "apellido_materno": "Matamoros",
                "gender": "F",
                "email": "kathy.vm@apizaco.tecnm.mx"
            },
            {
                "username": "adrian.tj",
                "first_name": "José Adrián",
                "last_name": "Trevera",
                "apellido_materno": "Juárez",
                "gender": "M",
                "email": "adrian.tj@apizaco.tecnm.mx"
            },
            {
                "username": "rosa.ca",
                "first_name": "Rosa",
                "last_name": "Cortes",
                "apellido_materno": "Aguirre",
                "gender": "F",
                "email": "rosa.ca@apizaco.tecnm.mx"
            },
            {
                "username": "crisanto.th",
                "first_name": "Crisanto",
                "last_name": "Tenopala",
                "apellido_materno": "Hernández",
                "gender": "M",
                "email": "crisanto.th@apizaco.tecnm.mx"
            },
            {
                "username": "alejandra.tl",
                "first_name": "Alejandra",
                "last_name": "Torres",
                "apellido_materno": "López",
                "gender": "F",
                "email": "alejandra.tl@apizaco.tecnm.mx"
            },
            {
                "username": "jorge.cg",
                "first_name": "Jorge Luis",
                "last_name": "Castañeda",
                "apellido_materno": "Gutiérrez",
                "gender": "M",
                "email": "jorge.cg@apizaco.tecnm.mx"
            },
            {
                "username": "elizabeth.mh",
                "first_name": "Elizabeth",
                "last_name": "Montiel",
                "apellido_materno": "Huerta",
                "gender": "F",
                "email": "elizabeth.mh@apizaco.tecnm.mx"
            },
            {
                "username": "hector.dm",
                "first_name": "Héctor",
                "last_name": "Domínguez",
                "apellido_materno": "Martínez",
                "gender": "M",
                "email": "hector.dm@apizaco.tecnm.mx"
            },
            {
                "username": "acela.dj",
                "first_name": "Acela",
                "last_name": "Dávila",
                "apellido_materno": "Jiménez",
                "gender": "F",
                "email": "acela.dj@apizaco.tecnm.mx"
            },
            {
                "username": "gerardo.it",
                "first_name": "Gerardo",
                "last_name": "Islas",
                "apellido_materno": "Téllez",
                "gender": "M",
                "email": "gerardo.it@apizaco.tecnm.mx"
            },
            {
                "username": "karla.gh",
                "first_name": "Karla",
                "last_name": "González",
                "apellido_materno": "Hidalgo",
                "gender": "F",
                "email": "karla.gh@apizaco.tecnm.mx"
            },
            {
                "username": "luis.mr",
                "first_name": "José Luis",
                "last_name": "Moreno",
                "apellido_materno": "Rivera",
                "gender": "M",
                "email": "luis.mr@apizaco.tecnm.mx"
            }
        ]

        # Crear o actualizar los docentes
        for docente in docentes_data:
            user, created = CustomUser.objects.get_or_create(
                username=docente['username'],
                defaults={
                    'first_name': docente['first_name'],
                    'last_name': docente['last_name'],
                    'apellido_materno': docente['apellido_materno'],
                    'gender': docente['gender'],
                    'email': docente['email'],
                    'password': make_password('12345'),
                    'is_superuser': False,
                    'is_staff': True  # Suponiendo que los docentes puedan necesitar acceso al panel administrativo
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Docente '{docente['first_name']}' creado exitosamente."))
                user.groups.add(grupo_docente)
                user.posgrado_docente.add(posgrado_admin)  # Asumiendo que posgrado_docente es un ManyToManyField
                user.save()
            else:
                self.stdout.write(self.style.WARNING(f"Docente '{docente['first_name']}' ya existe. No se realizaron cambios."))


    def cargar_docentes_mecatronica(self):
        grupo_docente, _ = Group.objects.get_or_create(name='Docente')
        posgrado_mecatronica, _ = Posgrado.objects.get_or_create(nombre="Maestría en Ingeniería Mecatrónica")

        # Datos de los docentes para Maestría en Ingeniería Mecatrónica
        docentes_data = [
            {
                "username": "rafael.of",
                "first_name": "Rafael",
                "last_name": "Ordoñez",
                "apellido_materno": "Flores",
                "gender": "M",
                "email": "rafael.of@apizaco.tecnm.mx"
            },
            {
                "username": "roberto.mc",
                "first_name": "Roberto",
                "last_name": "Morales",
                "apellido_materno": "Caporal",
                "gender": "M",
                "email": "roberto.mc@apizaco.tecnm.mx"
            },
            {
                "username": "vicente.fl",
                "first_name": "Vicente",
                "last_name": "Flores",
                "apellido_materno": "Lara",
                "gender": "M",
                "email": "vicente.fl@apizaco.tecnm.mx"
            },
            {
                "username": "jorge.bh",
                "first_name": "Jorge",
                "last_name": "Bedolla",
                "apellido_materno": "Hernández",
                "gender": "M",
                "email": "jorge.bh@apizaco.tecnm.mx"
            },
            {
                "username": "marcos.bh",
                "first_name": "Marcos",
                "last_name": "Bedolla",
                "apellido_materno": "Hernández",
                "gender": "M",
                "email": "marcos.bh@apizaco.tecnm.mx"
            },
            {
                "username": "francisco.hc2002",
                "first_name": "Francisco",
                "last_name": "Hernández",
                "apellido_materno": "Corona",
                "gender": "M",
                "email": "francisco_hc2002@hotmail.com"
            }
        ]

        # Crear o actualizar los docentes
        for docente in docentes_data:
            user, created = CustomUser.objects.get_or_create(
                username=docente['username'],
                defaults={
                    'first_name': docente['first_name'],
                    'last_name': docente['last_name'],
                    'apellido_materno': docente['apellido_materno'],
                    'gender': docente['gender'],
                    'email': docente['email'],
                    'password': make_password('initialPassword'),  # Asigna una contraseña inicial
                    'is_superuser': False,
                    'is_staff': True  # Suponiendo que los docentes puedan necesitar acceso al panel administrativo
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Docente '{docente['first_name']}' creado exitosamente."))
                user.groups.add(grupo_docente)
                user.posgrado_docente.add(posgrado_mecatronica)  # Asumiendo que posgrado_docente es un ManyToManyField
                user.save()
            else:
                self.stdout.write(self.style.WARNING(f"Docente '{docente['first_name']}' ya existe. No se realizaron cambios."))
