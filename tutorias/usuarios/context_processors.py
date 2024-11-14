# context_processors.py dentro de tu app, por ejemplo: myapp/context_processors.py
from django.contrib.auth.models import Group
from generales.models import Posgrado
from usuarios.models import Coordinador, TutorAlumno

def user_info(request):
    user_info_dict = {}
    if request.user.is_authenticated:
        # Nombre completo
        full_name = ' '.join(filter(None, [request.user.first_name, request.user.last_name, request.user.apellido_materno]))
        user_info_dict['user_name'] = request.user.username
        user_info_dict['full_name'] = full_name if full_name else 'Sin nombre especificado'
        
        # Género
        user_info_dict['user_gender'] = request.user.gender if hasattr(request.user, 'gender') else None
        
        # Posgrado para Alumno
        user_info_dict['posgrado_alumno'] = request.user.posgrado_alumno.nombre if request.user.posgrado_alumno else None
        
        # Posgrado para Coordinador
        try:
            coordinador = Coordinador.objects.get(usuario=request.user)
            user_info_dict['posgrado_coordinador'] = coordinador.posgrado.nombre
        except Coordinador.DoesNotExist:
            user_info_dict['posgrado_coordinador'] = None
        
        # Posgrados para Docente
        posgrados_docente = request.user.posgrado_docente.all()
        if posgrados_docente.exists():
            user_info_dict['posgrado_docente'] = [posgrado.nombre for posgrado in posgrados_docente]
        else:
            user_info_dict['posgrado_docente'] = []
        
        # Obtener Tutor
        try:
            tutor_alumno = TutorAlumno.objects.get(alumno=request.user)
            user_info_dict['tutor'] = tutor_alumno.tutor.get_full_name()
        except TutorAlumno.DoesNotExist:
            # Si no tiene tutor, intentar obtener el coordinador
            if request.user.posgrado_alumno:
                try:
                    coordinador = Coordinador.objects.get(posgrado=request.user.posgrado_alumno)
                    user_info_dict['tutor'] = f"Por favor, comunícate con tu coordinador: {coordinador.usuario.get_full_name()}"
                except Coordinador.DoesNotExist:
                    user_info_dict['tutor'] = "Por favor, comunícate con tu coordinador de tu posgrado."
            else:
                user_info_dict['tutor'] = "Posgrado no asignado."
    else:
        user_info_dict = {
            'user_name': None,
            'full_name': None,
            'user_gender': None,
            'posgrado_alumno': None,
            'posgrado_coordinador': None,
            'posgrado_docente': [],
            'tutor': None,
        }

    return {'user_info': user_info_dict}

def group_context(request):

    context = {
        'es_coordinador': request.user.groups.filter(name='Coordinador').exists(),
        'es_docente': request.user.groups.filter(name='Docente').exists(),
        'es_alumno': request.user.groups.filter(name='Alumno').exists(),
        'es_superusuario': request.user.is_superuser,  # Verificación para superusuario

    }
    return context