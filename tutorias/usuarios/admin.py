from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'apellido_materno', 'email', 'gender', 'posgrado_alumno')}),  # Añadido posgrado
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'apellido_materno', 'email', 'gender', 'posgrado_alumno', 'is_staff', 'is_active', 'groups'),  # Añadido posgrado
        }),
    )
    
    # Añadir 'posgrado' a list_display
    list_display = ('username', 'email', 'first_name', 'last_name', 'apellido_materno', 'gender_display', 'is_staff', 'display_posgrados')
    
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'gender', 'posgrado_alumno')  # Filtrar por posgrado

    def gender_display(self, obj):
        return obj.get_gender_display()
    gender_display.short_description = 'Género'

    # Función para mostrar los nombres de los posgrados en list_display
    def display_posgrados(self, obj):
        return ", ".join([p.nombre for p in obj.posgrado_alumno.all()])
    display_posgrados.short_description = 'Posgrado(s)'


admin.site.register(CustomUser, CustomUserAdmin)
