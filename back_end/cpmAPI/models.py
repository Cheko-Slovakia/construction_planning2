
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.oauth.oauth_manager import UserManager

# Create your models here.
class Test(models.Model):
    class Meta:
        db_table = 'Tests'
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=100)

class Trabajador(AbstractUser):
    objects = UserManager()
    USERNAME_FIELD = 'numero_cedula'
    REQUIRED_FIELDS = ['name', ]
    class Meta:
        db_table = 'Trabajadores'

    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    trabajador_id = models.AutoField(primary_key=True)
    numero_cedula = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    numero_celular = models.CharField(max_length=15)
    contrasena = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    obra_participante = models.IntegerField(default=0)


class Cliente(models.Model):
    class Meta:
        db_table = 'Clientes'
    cliente_id = models.AutoField(primary_key=True)
    numero_nit = models.CharField(max_length=30)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    direccion = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

class Material(models.Model):
    class Meta:
        db_table = 'Materiales'
    material_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    estado = models.CharField(max_length=50)

class Obra(models.Model):
    class Meta:
        db_table = 'Obras'

    obra_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    fase = models.CharField(max_length=1)
    latitud = models.FloatField()
    longitud = models.FloatField()
    trabajadores_participantes = models.ManyToManyField(Trabajador)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class InventarioObra(models.Model):
    class Meta:
        db_table = 'Obras_Materiales'

    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    aprobado = models.BooleanField(default=False)

class Avance(models.Model):
    class Meta:
        db_table = 'Avances'

    avance_id = models.AutoField(primary_key=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=500)
    link = models.CharField(max_length=2000)
    trabajador = models.CharField(default="", max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()
    tipo = models.IntegerField(default=1)
    fecha = models.DateField(default=now, blank=True)
    fase = models.CharField(default="3", max_length=1)
    aprobado = models.BooleanField(default=False)
