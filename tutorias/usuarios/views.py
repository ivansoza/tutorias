from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from generales.models import Posgrado
from usuarios.forms import CustomUserCreationFormUsuario
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from .models import CustomUser

# Create your views here.


class CoordinadoresListView(ListView):
    model = CustomUser
    template_name = 'users/coordinadores_list.html'
    context_object_name = 'coordinadores'

    def get_queryset(self):
        coordinadores_group = Group.objects.get(name='Coordinador')
        return CustomUser.objects.filter(groups=coordinadores_group)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'coordinador'
        return context
    
class DocentesListView(ListView):
    model = CustomUser
    template_name = 'users/docentes_list.html'
    context_object_name = 'docentes'

    def get_queryset(self):
        # Filtrar por grupo 'Docente'
        docentes_group = Group.objects.get(name='Docente')
        queryset = CustomUser.objects.filter(groups=docentes_group)

        # Filtrar por posgrado_docente si se proporciona el ID del posgrado a través del GET request
        posgrado_id = self.request.GET.get('posgrado_id')
        if posgrado_id:
            queryset = queryset.filter(posgrado_docente__id=posgrado_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtiene la queryset filtrada
        filtered_queryset = self.get_queryset()

        # Calcula el total de docentes activos en la queryset filtrada
        context['total_docentes'] = filtered_queryset.filter(is_active=True).count()

        # Calcula el total de maestrías y doctorados entre los docentes en la queryset filtrada
        context['total_maestria'] = filtered_queryset.filter(
            posgrado_docente__nombre__in=[
                "Maestría en Sistemas Computacionales",
                "Maestría en Ingeniería Mecatrónica",
                "Maestría en Ingeniería Administrativa"
            ]).count()

        context['total_doctorado'] = filtered_queryset.filter(
            posgrado_docente__nombre="Doctorado en Ciencias de la Ingeniería"
        ).count()

        # Añade los posgrados al contexto para el selector
        context['posgrados'] = Posgrado.objects.all()

        # Meta información de la página
        context['dashboard_title'] = 'Lista de Docentes'
        context['breadcrumb_active_item'] = 'Lista de Docente'
        context['navbar'] = 'docente'
        context['url'] = 'home'

        return context


class AlumnosListView(ListView):
    model = CustomUser
    template_name = 'users/alumnos_list.html'
    context_object_name = 'alumnos'

    def get_queryset(self):
        # Filtrar por grupo 'Alumno'
        alumnos_group = Group.objects.get(name='Alumno')
        queryset = CustomUser.objects.filter(groups=alumnos_group)
        
        # Filtrar por posgrado_alumno si se proporciona el ID del posgrado a través del GET request
        posgrado_id = self.request.GET.get('posgrado_id')
        if posgrado_id:
            queryset = queryset.filter(posgrado_alumno__id=posgrado_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene la queryset filtrada
        filtered_queryset = self.get_queryset()
        
        # Calcula el total de estudiantes activos en la queryset filtrada
        context['total_estudiantes'] = filtered_queryset.filter(is_active=True).count()
        
        # Calcula el total de maestría y doctorado en la queryset filtrada
        context['total_maestria'] = filtered_queryset.filter(
            posgrado_alumno__nombre__in=[
                "Maestría en Sistemas Computacionales",
                "Maestría en Ingeniería Mecatrónica",
                "Maestría en Ingeniería Administrativa"
            ]).count()
        
        context['total_doctorado'] = filtered_queryset.filter(
            posgrado_alumno__nombre="Doctorado en Ciencias de la Ingeniería"
        ).count()
        
        # Añade los posgrados al contexto para el selector
        context['posgrados'] = Posgrado.objects.all()

        # Meta información de la página
        context['dashboard_title'] = 'Lista de Alumnos'
        context['breadcrumb_active_item'] = 'Lista de Alumno'
        context['navbar'] = 'alumno'
        context['url'] = 'home'
        
        return context





class CustomUserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationFormUsuario
    template_name = 'registerUser.html'
    success_url = reverse_lazy('alumnos-list')  
    def form_valid(self, form):
        # Guardar el usuario para asignar un ID antes de agregar grupos
        user = form.save(commit=False)
        
        # Guardar el usuario completamente en la base de datos
        user.save()

        # Agregar al grupo "Alumno"
        grupo, created = Group.objects.get_or_create(name='Alumno')
        user.groups.add(grupo)
        messages.success(self.request, "Alumno agregado con éxito.")
        return super().form_valid(form)



    def form_invalid(self, form):
        messages.error(self.request, "Error al agregar el usuario. Por favor, corrija los errores en el formulario.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = 'alumnos-list'
        context['breadcrumb_active_item'] = 'Registrar Alumno'
        context['navbar'] = 'alumno'
        return context