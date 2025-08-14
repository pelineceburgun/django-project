from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Message

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            return render(request, 'accounts/login.html', {'error': 'Kullanıcı adı veya şifre yanlış!'})
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {'error': 'Bu kullanıcı adı zaten alınmış!'})
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return render(request, 'accounts/signup.html', {'message': 'Kayıt başarılı! Şimdi giriş yapabilirsiniz.'})
    return render(request, 'accounts/signup.html')

def welcome_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # Kullanıcının mesajlarını al
    messages = Message.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/welcome.html', {
        'username': request.user.username,
        'messages': messages
    })

def logout_view(request):
    logout(request)
    return redirect('login')

def handle_action(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'showMessage':
            return JsonResponse({'result': 'Merhaba! Bu bir test mesajıdır.'})
        elif action == 'changeColor':
            return JsonResponse({'result': 'Arka plan rengi değiştirildi!'})
        elif action == 'showInfo':
            return JsonResponse({'result': f'Kullanıcı: {request.user.username}, Giriş Zamanı: {request.user.last_login}'})
    return JsonResponse({'result': ''})

def submit_message(request):
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('message')
        if content:
            Message.objects.create(user=request.user, content=content)
            return redirect('welcome')
        else:
            return render(request, 'accounts/welcome.html', {
                'username': request.user.username,
                'messages': Message.objects.filter(user=request.user).order_by('-created_at'),
                'error': 'Mesaj boş olamaz!'
            })
    return redirect('welcome')