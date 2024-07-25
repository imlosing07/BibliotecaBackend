from datetime import date, timedelta
from rest_framework import serializers
from .models import Alumno, Libro, Notificacion, Prestamo, Reporte, Reserva, Usuario

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['dni', 'nombres', 'apellidoPat', 'apellidoMat', 'estado']

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    usuarioReserva = UsuarioSerializer()  # Nested serializer for Usuario
    libroReserva = LibroSerializer()  # Nested serializer for Libro

    class Meta:
        model = Reserva
        fields = '__all__'

class ReservaCreateSerializer(serializers.Serializer):
    isbn = serializers.CharField(max_length=13)
    dni = serializers.CharField(max_length=8)
    fechaReserva = serializers.DateField(required=False)

    def create(self, validated_data):
        isbn = validated_data['isbn']
        dni = validated_data['dni']

        # Buscar libro y usuario
        try:
            libro = Libro.objects.get(isbn=isbn)
        except Libro.DoesNotExist:
            raise serializers.ValidationError("Libro no encontrado.")

        try:
            usuario = Usuario.objects.get(dni=dni)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Alumno no encontrado.")

        # Establecer fechas, usar fecha actual y una fecha de devolución por defecto (e.g., 14 días después)
        fecha_reserva = validated_data.get('fechaReserva', date.today())

        # Crear prestamo
        reserva = Reserva.objects.create(
            libroReserva=libro, 
            usuarioReserva=usuario, 
            fechaReserva=fecha_reserva,
            estado='reservado'  # Asigna un estado por defecto
        )
        return reserva

class PrestamoSerializer(serializers.ModelSerializer):
    alumnoPrestado = AlumnoSerializer()  # Nested serializer for Usuario
    libroPrestado = LibroSerializer()  # Nested serializer for Libro
    class Meta:
        model = Prestamo
        fields = '__all__'
        
class PrestamoCreateSerializer(serializers.Serializer):
    isbn = serializers.CharField(max_length=13)
    dni = serializers.CharField(max_length=8)
    fechaPrestamo = serializers.DateField(required=False)
    fechaDevolucion = serializers.DateField(required=False)

    def create(self, validated_data):
        isbn = validated_data['isbn']
        dni = validated_data['dni']

        # Buscar libro y usuario
        try:
            libro = Libro.objects.get(isbn=isbn)
        except Libro.DoesNotExist:
            raise serializers.ValidationError("Libro no encontrado.")

        try:
            alumno = Alumno.objects.get(dni=dni)
        except Alumno.DoesNotExist:
            raise serializers.ValidationError("Alumno no encontrado.")

        # Establecer fechas, usar fecha actual y una fecha de devolución por defecto (e.g., 14 días después)
        fecha_prestamo = validated_data.get('fechaPrestamo', date.today())
        fecha_devolucion = validated_data.get('fechaDevolucion', date.today() + timedelta(days=14))

        # Crear prestamo
        prestamo = Prestamo.objects.create(
            libroPrestado=libro, 
            alumnoPrestado=alumno, 
            fechaPrestamo=fecha_prestamo, 
            fechaDevolucion=fecha_devolucion,
            estado='pendiente'  # Asigna un estado por defecto
        )
        return prestamo
    
class ReservaUpdateSerializer(serializers.Serializer):
    isbn = serializers.CharField(max_length=13)
    dni = serializers.CharField(max_length=8)
    fechaReserva = serializers.DateField(required=False)
    estado = serializers.CharField(max_length=20, required=False)

    def update(self, instance, validated_data):
        isbn = validated_data.get('isbn', instance.libroReserva.isbn)
        dni = validated_data.get('dni', instance.usuarioReserva.dni)

        # Buscar libro y usuario
        try:
            libro = Libro.objects.get(isbn=isbn)
            instance.libroReserva = libro
        except Libro.DoesNotExist:
            raise serializers.ValidationError("Libro no encontrado.")

        try:
            usuario = Usuario.objects.get(dni=dni)
            instance.usuarioReserva = usuario
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado.")

        instance.fechaReserva = validated_data.get('fechaReserva', instance.fechaReserva)
        instance.estado = validated_data.get('estado', instance.estado)

        instance.save()
        return instance

class PrestamoUpdateSerializer(serializers.Serializer):
    isbn = serializers.CharField(max_length=13)
    dni = serializers.CharField(max_length=8)
    fechaPrestamo = serializers.DateField(required=False)
    fechaDevolucion = serializers.DateField(required=False)
    estado = serializers.CharField(max_length=20, required=False)

    def update(self, instance, validated_data):
        isbn = validated_data.get('isbn', instance.libroPrestado.isbn)
        dni = validated_data.get('dni', instance.alumnoPrestado.dni)

        # Buscar libro y alumno
        try:
            libro = Libro.objects.get(isbn=isbn)
            instance.libroPrestado = libro
        except Libro.DoesNotExist:
            raise serializers.ValidationError("Libro no encontrado.")

        try:
            alumno = Alumno.objects.get(dni=dni)
            instance.alumnoPrestado = alumno
        except Alumno.DoesNotExist:
            raise serializers.ValidationError("Alumno no encontrado.")

        instance.fechaPrestamo = validated_data.get('fechaPrestamo', instance.fechaPrestamo)
        instance.fechaDevolucion = validated_data.get('fechaDevolucion', instance.fechaDevolucion)
        instance.estado = validated_data.get('estado', instance.estado)

        instance.save()
        return instance