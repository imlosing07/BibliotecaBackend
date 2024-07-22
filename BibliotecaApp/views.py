from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from .forms import LoginForm

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contraseña = form.cleaned_data['contraseña']
            
            try:
                usuario = Usuario.objects.get(correo=correo)
                if usuario.check_password(contraseña):
                    request.session['usuario_id'] = usuario.id
                    messages.success(request, "Inicio de sesión exitoso")
                    return redirect('home')
                else:
                    messages.error(request, "Correo o contraseña incorrectos")
            except Usuario.DoesNotExist:
                messages.error(request, "Correo o contraseña incorrectos")
    else:
        form = LoginForm()
    
    return render(request, 'BibliotecaApp/login.html', {'form': form})

def home_view(request):
    return render(request, 'BibliotecaApp/home.html')
