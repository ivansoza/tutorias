from django.urls import path
from .views import CoordinadoresListView, CustomTeacherCreateView, CustomTeacherEditView, CustomUserCreateView, CustomUserEditView, DocentesListView, AlumnosListView

urlpatterns = [
    path('coordinadores/', CoordinadoresListView.as_view(), name='coordinadores-list'),
    path('docentes/', DocentesListView.as_view(), name='docentes-list'),
    path('alumnos/', AlumnosListView.as_view(), name='alumnos-list'),

    path('register/', CustomUserCreateView.as_view(), name='register_user'),
    path('editar-usuario/<int:pk>/', CustomUserEditView.as_view(), name='editar-usuario'),

    path('register-docente/', CustomTeacherCreateView.as_view(), name='register_user_docente'),
    path('editar-docente/<int:pk>/', CustomTeacherEditView.as_view(), name='editar-docente'),

]
