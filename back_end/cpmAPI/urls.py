from django.conf.urls import url
from cpmAPI import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^tests/$', views.testApi),
    url(r'^tests/([0-9]+)$', views.testApi),

    url(r'^SaveFile$', views.SaveFile),

    #Trabajadores
    url(r'^trabajadores/$', views.trabajadorAPI),
    url(r'^trabajadores/([0-9]+)$', views.trabajadorAPI),
    url(r'^trabajadores/([A-Za-z]+)$', views.trabajadorAPI),

    url(r'^clientes/$', views.clienteAPI),
    url(r'^clientes/([0-9]+)$', views.clienteAPI),
    url(r'^clientes/([A-Za-z]+)$', views.clienteAPI),

    url(r'^obras/$', views.obraAPI),
    url(r'^obras/([0-9]+)$', views.obraAPI),

    url(r'^obras/trabajadores/$', views.obraTrabajadorAPI),
    url(r'^obras/trabajadores/([0-9]+)/$', views.obraTrabajadorAPI),

    url(r'^obras/clientes/$', views.obraClienteAPI),
    url(r'^obras/clientes/([0-9]+)/$', views.obraClienteAPI),

    url(r'^obras/avances/$', views.avanceAPI),
    url(r'^obras/avances/([0-9]+)/$', views.avanceAPI),

    url(r'^obras/materiales/$', views.obraMaterialesAPI),
    url(r'^obras/materiales/([0-9]+)/$', views.obraMaterialesAPI),

    url(r'^materiales/$', views.materialAPI),
    url(r'^materiales/([0-9]+)/$', views.materialAPI),

    url(r'^validacion/obras/$', views.validacionObrasAPI),
    url(r'^validacion/solicitudes/$', views.validacionSolicitudesAPI),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)