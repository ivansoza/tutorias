from django.urls import path
from .views import AlumnoDetailView, CoordinadoresListView, CustomTeacherCreateView, CustomTeacherEditView, CustomUserCreateView, CustomUserEditView, DocentesListView, AlumnosListView, PosgradosListView, asignar_coordinador, asignar_tutor, eliminar_alumno, eliminar_docente, get_docentes, get_docentes_by_alumno, retirar_coordinador

urlpatterns = [
    path('coordinadores/', CoordinadoresListView.as_view(), name='coordinadores-list'),
    path('docentes/', DocentesListView.as_view(), name='docentes-list'),
    path('alumnos/', AlumnosListView.as_view(), name='alumnos-list'),

    path('register/', CustomUserCreateView.as_view(), name='register_user'),
    path('editar-usuario/<int:pk>/', CustomUserEditView.as_view(), name='editar-usuario'),
    path('alumnos/eliminar/<int:user_id>/', eliminar_alumno, name='eliminar-alumno'),

    path('register-docente/', CustomTeacherCreateView.as_view(), name='register_user_docente'),
    path('editar-docente/<int:pk>/', CustomTeacherEditView.as_view(), name='editar-docente'),
    path('posgrados/', PosgradosListView.as_view(), name='posgrados_list'),
    path('get-docentes/', get_docentes, name='get-docentes'),
    path('asignar-coordinador/', asignar_coordinador, name='asignar-coordinador'),
    path('retirar-coordinador/<int:posgrado_id>/', retirar_coordinador, name='retirar-coordinador'),
    path('eliminar-docente/<int:user_id>/', eliminar_docente, name='eliminar-docente'),
    path('get-docentes/<int:user_id>/', get_docentes_by_alumno, name='get-docentes-by-alumno'),
    path('asignar-tutor/', asignar_tutor, name='asignar-tutor'),
    path('alumnos/detalle/<int:pk>/', AlumnoDetailView.as_view(), name='alumno-detail'),

]
