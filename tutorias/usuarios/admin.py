from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TutorAlumno, Semestre, Anexo1, Anexo2, Anexo3





admin.site.register(CustomUser)
admin.site.register(Semestre)
admin.site.register(Anexo1)
admin.site.register(Anexo2)
admin.site.register(Anexo3)
@admin.register(TutorAlumno)
class TutorAlumnoAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'alumno')
    search_fields = ('tutor__username', 'alumno__username')
    raw_id_fields = ('tutor', 'alumno')  # Esto puede ser útil si tienes muchos usuarios