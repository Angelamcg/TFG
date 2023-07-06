from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100)
    cif = models.CharField(max_length=9, unique=True)
    email = models.EmailField()
    telefono = PhoneNumberField()
    web = models.URLField()

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        ordering = ['nombre_empresa']


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100)
    cif = models.CharField(max_length=9, unique=True)
    email = models.EmailField()
    telefono = PhoneNumberField()
    web = models.URLField()

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        ordering = ['nombre_empresa']

# PhoneNumberField instalado en settings.py

# Ubicaciones
class Almacen(models.Model):
    id = models.AutoField(primary_key=True)
    pasillo = models.CharField(max_length=20)
    seccion = models.CharField(max_length=20)
    altura = models.CharField(max_length=20)

    class Meta:
        ordering = ['pasillo', 'seccion', 'altura']

class Plano(models.Model):
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='almacen/')
    pasillos = models.IntegerField()
    secciones = models.IntegerField()
    alturas = models.IntegerField()

    def save(self, *args, **kwargs):
        # Asegurar que solo haya un objeto Plano en la base de datos
        if not self.pk and Plano.objects.exists():
            existing_plano = Plano.objects.first()
            existing_plano.delete()

        super().save(*args, **kwargs)

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    referencia = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    precio_minorista = models.DecimalField(max_digits=8, decimal_places=2)
    precio_mayorista = models.DecimalField(max_digits=8, decimal_places=2)
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    fotografia = models.ImageField(upload_to='productos/')
    id_ubicacion = models.ForeignKey(Almacen, null=True, blank=True, on_delete=models.CASCADE)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ['fecha']

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ManyToManyField(Producto, through='FilaVenta')
    fecha = models.DateTimeField(default=timezone.now)
    id_cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ['fecha']


class FilaVenta(models.Model):
    id = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_venta = models.IntegerField()
    precio_venta = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ['id']

class Devolucion(models.Model):
    id = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    razon = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ['fecha']


class FilaDevolucion(models.Model):
    id = models.AutoField(primary_key=True)
    devolucion = models.ForeignKey(Devolucion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_devuelta = models.IntegerField()

    class Meta:
        ordering = ['id']

