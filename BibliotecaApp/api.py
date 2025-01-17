from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Alumno, Libro, Notificacion, Reporte, Usuario, Reserva, Prestamo
from .serializers import PrestamoDetailSerializer, ReservaDetailSerializer, ReservaUpdateSerializer, AlumnoSerializer, LibroSerializer, NotificacionSerializer, PrestamoCreateSerializer, PrestamoUpdateSerializer, ReporteSerializer, ReservaCreateSerializer, UsuarioSerializer, ReservaSerializer, PrestamoSerializer

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

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PrestamoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PrestamoUpdateSerializer
        return PrestamoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prestamo = serializer.save()
        return Response(PrestamoSerializer(prestamo).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ReservaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ReservaUpdateSerializer
        return ReservaDetailSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()