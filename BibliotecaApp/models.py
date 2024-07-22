from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    dni = models.CharField(max_length=8, primary_key=True, unique=True, null=False)
    nombres = models.CharField(max_length=75)
    apellidoPat = models.CharField(max_length=50)
    apellidoMat = models.CharField(max_length=50)
    correo = models.EmailField()
    contraseña = models.CharField(max_length=128)
    fechaCreada = models.DateTimeField(auto_now_add=True)
    estado = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        if self.pk is None or 'contraseña' in self.changed_data:  # Solo encriptamos si es nuevo o si se cambia la contraseña
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)
        
    def check_password(self, password):
        return check_password(password, self.contraseña)
    
class Alumno(models.Model):
    dni = models.CharField(max_length=8, primary_key=True, unique=True, null=False)
    nombres = models.CharField(max_length=75)
    apellidoPat = models.CharField(max_length=50)
    apellidoMat = models.CharField(max_length=50)
    estado = models.IntegerField(default=1)

class Libro(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True, unique=True, null=False)
    titulo = models.CharField()
    autor = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    cantidad = models.IntegerField(default=0)
    estado = models.IntegerField(default=1)
    
class Reserva(models.Model):
    fechaReserva = models.DateField()
    usuarioReserva = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libroReserva = models.ForeignKey(Libro, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20)
    
class Prestamo(models.Model):
    alumnoPrestado = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    libroPrestado = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fechaPrestamo = models.DateField()
    fechaDevolucion = models.DateField()
    estado = models.CharField(max_length=20)

class Notificacion(models.Model):
    mensaje = models.TextField()
    fechaCreada = models.DateTimeField(auto_now_add=True)
    
class Reporte(models.Model):
    tipoReporte = models.CharField(max_length=20)
    contenido = models.TextField()
    fechaCreada = models.DateTimeField(auto_now_add=True)
 
    
    
    

    

