from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import DeviceInstance, DeviceBookingCalendar
from .serializers import DeviceInstanceSerializer, DeviceBookingCalendarSerializer
from .forms import LoginForm, RegistrationForm

class DeviceInstanceViewSet(viewsets.ModelViewSet):
    queryset = DeviceInstance.objects.all()
    serializer_class = DeviceInstanceSerializer

class DeviceBookingCalendarViewSet(viewsets.ModelViewSet):
    queryset = DeviceBookingCalendar.objects.all()
    serializer_class = DeviceBookingCalendarSerializer
    filterset_fields = ['device_instance']

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/booking/')
            else:
                form.add_error('password', 'Incorrect username or password')
    else:
        form = LoginForm()
    return render(request, 'booking/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # save user to database and login automatically
            user = form.save()
            login(request, user)
            return redirect('/booking/')
    else:
        form = RegistrationForm()
    return render(request, 'booking/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('/login/')

