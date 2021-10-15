from django.contrib import admin
import cpmAPI.management.commands.seed as seed
from cpmAPI.models import Trabajador, Cliente

#seed.clear_data()
test = len(Trabajador.objects.all())
if len(Trabajador.objects.all()) == 0:
    seed.create_trabajadores()
if len(Cliente.objects.all()) == 0:
    seed.create_clientes()



