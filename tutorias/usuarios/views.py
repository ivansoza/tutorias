from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from generales.models import Posgrado
from usuarios.forms import CustomUserCreationFormDocente, CustomUserCreationFormUsuario, CustomUserEditForm, CustomUserEditFormDocente
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from .models import CustomUser
from django.db.models import Count, Q
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse

from django.shortcuts import get_object_or_404, redirect

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
        docentes_group = Group.objects.get(name='Docente')
        queryset = CustomUser.objects.filter(groups=docentes_group)

        posgrado_id = self.request.GET.get('posgrado_id')
        if posgrado_id:
            queryset = queryset.filter(posgrado_docente__id=posgrado_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filtered_queryset = self.get_queryset()

        context['total_docentes'] = filtered_queryset.filter(is_active=True).count()

        context['total_maestria'] = filtered_queryset.filter(
            posgrado_docente__nombre__in=[
                "Maestría en Sistemas Computacionales",
                "Maestría en Ingeniería Mecatrónica",
                "Maestría en Ingeniería Administrativa"
            ]
        ).distinct().count()

        context['total_doctorado'] = filtered_queryset.filter(
            posgrado_docente__nombre="Doctorado en Ciencias de la Ingeniería"
        ).distinct().count()

        context['posgrados'] = Posgrado.objects.all()
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
        user = form.save(commit=False)
        user.save()
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
    

class CustomUserEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'editUser.html'  # Debes crear esta plantilla
    success_url = reverse_lazy('alumnos-list')  # Ajusta según sea necesario

    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado con éxito.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el usuario. Por favor, corrija los errores en el formulario.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = 'alumnos-list'  # O la URL adecuada
        context['breadcrumb_active_item'] = 'Editar Usuario'
        context['navbar'] = 'alumno'
        return context

class CustomTeacherCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationFormDocente
    template_name = 'registerUserDocente.html'
    success_url = reverse_lazy('docentes-list')  # Cambiado a la lista de docentes
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        grupo, created = Group.objects.get_or_create(name='Docente')  # Cambiado a grupo Docente
        user.groups.add(grupo)
        messages.success(self.request, "Docente agregado con éxito.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al agregar el docente. Por favor, corrija los errores en el formulario.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = 'docentes-list' 
        context['breadcrumb_active_item'] = 'Registrar Docente' 
        context['navbar'] = 'docente' 
        return context

class CustomTeacherEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserEditFormDocente
    template_name = 'editUserDocente.html'  # Asegúrate de crear esta plantilla
    success_url = reverse_lazy('docentes-list')
    success_message = "Docente actualizado con éxito."

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el docente. Por favor, corrija los errores en el formulario.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = 'docentes-list'
        context['breadcrumb_active_item'] = 'Editar Docente'
        context['navbar'] = 'docente'
        return context


def eliminar_alumno(request, user_id):
    alumno = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == "POST":
        alumno.delete()
        messages.success(request, f"El alumno {alumno.get_full_name()} ha sido eliminado exitosamente.")
        return redirect(reverse('alumnos-list'))
    
    return redirect('alumnos-list')