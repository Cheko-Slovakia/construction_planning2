# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand
import logging, os, random
from cpmAPI.models import Trabajador, Cliente
import pandas as pd
from django.db import connection
from django.contrib.auth.hashers import make_password


# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    logging.info("Delete Address instances")
    Trabajador.objects.all().delete()
    Cliente.objects.all().delete()


def create_trabajadores():
    """Creates an address object combining different elements from the list"""
    logging.info("Creating address")
    df = pd.read_excel(os.path.normpath("cpmAPI/management/seed_data/trabajadores.xlsx"))
    df['numero_cedula'] = df['numero_cedula'].astype(str)
    df['contrasena'] = df['contrasena'].astype(str)
    cargos = ["OBRERO", "ADMINISTRADOR", "JEFE_ALMACEN"]

    for i in range(len(df.index)):
        new_trabajador = Trabajador.objects.create(
            numero_cedula=df.numero_cedula[i],
            nombre=df.nombre[i],
            apellido=df.apellido[i],
            direccion=df.direccion[i],
            numero_celular=df.numero_celular[i],
            contrasena='',
            cargo=random.choice(cargos),
            username=df.numero_cedula[i],
            password=make_password(df.contrasena[i])
        )
        new_trabajador.save()
        print("Trabajador " + df.numero_cedula[i] + " creado satisfactoriamente")


    #logging.info("{} address created.".format(address))
    #return address

def create_clientes():
    """Creates an address object combining different elements from the list"""
    logging.info("Creating address")
    df = pd.read_excel(os.path.normpath("cpmAPI/management/seed_data/clientes.xlsx"))
    df['numero_nit'] = df['numero_nit'].astype(str)

    print(df.info())
    cargos = ["SUPERVISOR"]
    query = """INSERT INTO Clientes (numero_nit, 
                                         nombre,
                                         apellido,
                                         correo,
                                         direccion,
                                         contrasena,
                                         cargo,
                                         is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, True)"""

    #df.to_sql("Trabajadores", con=sql.connect("db.sqlite3"))
    with connection.cursor() as cursor:
        for i in range(len(df.index)):
            print([df.numero_nit[i],
                                df.nombre[i],
                                df.apellido[i],
                                df.correo[i],
                                df.direccion[i],
                                df.contrasena[i],
                                random.choice(cargos)])

            cursor.execute(query, (df.numero_nit[i],
                                   df.nombre[i],
                                   df.apellido[i],
                                   df.correo[i],
                                   df.direccion[i],
                                   df.contrasena[i],
                                   random.choice(cargos)))

        cursor.close()

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating 15 addresses
    create_trabajadores()