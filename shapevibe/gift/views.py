from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import GiftForm, UserForm
from .models import Gift

# Create your views here.
def index(request):
    all_gifts = Gift.objects.all()  # or filter by user
    # query = request.GET.get("q")
    return render(request, 'gift/index.html', {'all_gifts': all_gifts})

def detail(request, gift_id):
    user = request.user
    gift = get_object_or_404(Gift, pk=gift_id)
    return render(request, 'gift/detail.html', {'gift': gift, 'user': user})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'gift/login.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                gifts = Gift.objects.all() #or filter by user
                return render(request, 'gift/index.html', {'gifts': gifts, 'user':user})
            else:
                return render(request, 'gift/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'gift/login.html', {'error_message': 'Invalid login'})
    return render(request, 'gift/login.html')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                gifts = Gift.objects.all() # or filter by user
                return render(request, 'gift/index.html', {'gifts': gifts})
    context = {
        "form": form,
    }
    return render(request, 'gift/register.html', context)

