from django.urls import path

from .views import Anexo2, Anexo3, AnexosView, GenerarPDF


urlpatterns = [

    path('export/', GenerarPDF.as_view(), name="export_pdf"),
    path('anexo2/', Anexo2.as_view(), name="anexo2"),
    path('anexo3/', Anexo3.as_view(), name="anexo3"),

    path('anexos/', AnexosView.as_view(), name="anexos-view")

]
