from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Alumno, Libro, Notificacion, Reporte, Usuario, Reserva, Prestamo
from .serializers import AlumnoSerializer, LibroSerializer, NotificacionSerializer, PrestamoCreateSerializer, ReporteSerializer, ReservaCreateSerializer, UsuarioSerializer, ReservaSerializer, PrestamoSerializer

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
            return ReservaCreateSerializer
        return ReservaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reserva = serializer.save()
        return Response(ReservaSerializer(reserva).data, status=status.HTTP_201_CREATED)

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PrestamoCreateSerializer
        return PrestamoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prestamo = serializer.save()
        return Response(PrestamoSerializer(prestamo).data, status=status.HTTP_201_CREATED)
