from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TutorAlumno





admin.site.register(CustomUser)
@admin.register(TutorAlumno)
class TutorAlumnoAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'alumno')
    search_fields = ('tutor__username', 'alumno__username')
    raw_id_fields = ('tutor', 'alumno')  # Esto puede ser útil si tienes muchos usuarios