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
            alumno = Alumno.objects.get(dni=dni)
        except Alumno.DoesNotExist:
            raise serializers.ValidationError("Alumno no encontrado.")

        # Establecer fechas, usar fecha actual y una fecha de devolución por defecto (e.g., 14 días después)
        fecha_reserva = validated_data.get('fechaReserva', date.today())

        # Crear prestamo
        reserva = Reserva.objects.create(
            libroReserva=libro, 
            alumnoReserva=alumno, 
            fechaReserva=fecha_reserva,
            estado='reservado'  # Asigna un estado por defecto
        )
        return reserva

class ReservaDetailSerializer(serializers.ModelSerializer):
    libroReserva = LibroSerializer()
    alumnoReserva = AlumnoSerializer()

    class Meta:
        model = Reserva
        fields = ['id', 'libroReserva', 'alumnoReserva', 'fechaReserva', 'estado']

class ReservaUpdateSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=13, required=False, write_only=True)
    dni = serializers.CharField(max_length=8, required=False, write_only=True)

    class Meta:
        model = Reserva
        fields = ['isbn', 'dni', 'fechaReserva', 'estado']

    def to_representation(self, instance):
        # Este método controla cómo se muestra el objeto en las respuestas
        return ReservaDetailSerializer(instance).data

    def update(self, instance, validated_data):
        isbn = validated_data.pop('isbn', None)
        dni = validated_data.pop('dni', None)

        if isbn:
            try:
                libro = Libro.objects.get(isbn=isbn)
                instance.libroReserva = libro
            except Libro.DoesNotExist:
                raise serializers.ValidationError("Libro no encontrado.")

        if dni:
            try:
                alumno = Alumno.objects.get(dni=dni)
                instance.alumnoReserva = alumno
            except Alumno.DoesNotExist:
                raise serializers.ValidationError("Alumno no encontrado.")

        return super().update(instance, validated_data)

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

class PrestamoDetailSerializer(serializers.ModelSerializer):
    libroPrestado = LibroSerializer()
    alumnoPrestado = AlumnoSerializer()

    class Meta:
        model = Prestamo
        fields = ['id', 'libroPrestado', 'alumnoPrestado', 'fechaPrestamo', 'fechaDevolucion', 'estado']

class PrestamoUpdateSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(max_length=13, required=False, write_only=True)
    dni = serializers.CharField(max_length=8, required=False, write_only=True)

    class Meta:
        model = Prestamo
        fields = ['isbn', 'dni', 'fechaPrestamo', 'fechaDevolucion', 'estado']

    def to_representation(self, instance):
        return PrestamoSerializer(instance).data

    def update(self, instance, validated_data):
        isbn = validated_data.pop('isbn', None)
        dni = validated_data.pop('dni', None)

        if isbn:
            try:
                libro = Libro.objects.get(isbn=isbn)
                instance.libroPrestado = libro
            except Libro.DoesNotExist:
                raise serializers.ValidationError("Libro no encontrado.")

        if dni:
            try:
                alumno = Alumno.objects.get(dni=dni)
                instance.alumnoPrestado = alumno
            except Alumno.DoesNotExist:
                raise serializers.ValidationError("Alumno no encontrado.")

        return super().update(instance, validated_data)