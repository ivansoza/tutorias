# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
from django.views.generic import TemplateView

from weasyprint import HTML
# from weasyprint.fonts import FontConfiguration

class GenerarPDF(View):
    def get(self, request, *args, **kwargs):
        contexto = {
            'mensaje': 'Este es un PDF de ejemplo generado con WeasyPrint en Django.',
        }
        html_string = render_to_string("anexos/anexo1.html", contexto)        
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mi_documento.pdf"'

        return response
    
class Anexo2(View):
    def get(self, request, *args, **kwargs):
        contexto = {
            'mensaje': 'Este es un PDF de ejemplo generado con WeasyPrint en Django.',
        }
        html_string = render_to_string("anexos/anexo2.html", contexto)        
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mi_documento.pdf"'

        return response
    
class Anexo3(View):
    def get(self, request, *args, **kwargs):
        contexto = {
            'mensaje': 'Este es un PDF de ejemplo generado con WeasyPrint en Django.',
        }
        html_string = render_to_string("anexos/anexo3.html", contexto)        
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mi_documento.pdf"'

        return response
    
class AnexosView(TemplateView):
    template_name = 'anexos.html'  # Asegúrate de tener esta plantilla en tu directorio de templates

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'anexos'
                
                
        context['url'] = 'home'

        return context



