from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.db.models import Q
from .tokens import account_activation_token
from .forms import GiftForm, UserForm, SignupForm,ProfileForm
from .models import Gift
import datetime

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


# Create your views here.
def about(request):
    return render(request, 'gift/about.html')


@login_required
def index(request):
    user = request.user
    gifts = Gift.objects.all().order_by('-id')  # or filter by user
    users = User.objects.all()
    query = request.GET.get("q")
    if query:
        # soon will filter by tags as well
        gifts = Gift.objects.filter(
            Q(gift_title__icontains=query) |
            Q(gift_description__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()
        users = users.filter(
            Q(username__contains=query) |
            Q(profile__first_name__iexact=query) |
            Q(profile__last_name__iexact=query) |
            Q(profile__first_name__contains=query, profile__last_name__contains=query) |
            Q(profile__tags__icontains=query)
        ).distinct()
        return render(request, 'gift/index.html', {'gifts': gifts, 'users': users, 'query': query})
    else:
        return render(request, 'gift/index.html', {'user': user, 'gifts': gifts})

@login_required
def detail(request, gift_id):
    user = request.user
    gift = get_object_or_404(Gift, pk=gift_id)
    return render(request, 'gift/detail.html', {'gift': gift, 'user': user})

@login_required
def modal(request, gift_id):
    user = request.user
    gift = get_object_or_404(Gift, pk=gift_id)
    return render(request, 'gift/modal.html', {'gift': gift, 'user': user})

# CREATE, UPDATE, DELETE GIFT
@login_required
def create_gift(request):
    if request.method == 'POST':
        form = GiftForm(request.POST, request.FILES)
        if form.is_valid():
            gift = form.save(commit=False)
            gift.user = request.user
            if gift.gift_image:
                file_type = gift.gift_image.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    context = {
                        'gift': gift,
                        'form': form,
                        'error_message': 'Image file must be PNG, JPG, or JPEG',
                    }
                    return render(request, 'gift/create_gift.html', context)
            gift.save()
            return render(request, 'gift/detail.html', {'gift': gift})
    else:
        form = GiftForm()
    return render(request, 'gift/create_gift.html', {'form': form})

@login_required
def edit_gift(request, gift_id):
    gift = get_object_or_404(Gift, pk=gift_id)
    viber = gift.user
    if request.user != viber:
        return redirect('gift:detail', gift_id=gift_id)
    if request.method == 'POST':
        form = GiftForm(request.POST, request.FILES, instance=gift)
        try:
            if form.is_valid():
                gift = form.save(commit=False)
                if gift.gift_image:
                    file_type = gift.gift_image.url.split('.')[-1]
                    file_type = file_type.lower()
                    if file_type not in IMAGE_FILE_TYPES:
                        context = {
                            'gift': gift,
                            'form': form,
                            'error_message': 'Image file must be PNG, JPG, or JPEG',
                        }
                        return render(request, 'gift/edit_gift.html', context)
                gift.save()
                return render(request, 'gift/detail.html', {'gift': gift, 'success_message':'Succesffully edited gift.'})
        except:
            context = {
                'gift': gift,
                'form': form,
                'error_message': 'Error editing gift',
            }
            return render(reqnest, 'gift/edit_gift.html', context)
    else:
        form = GiftForm(instance=gift)
        return render(request, 'gift/edit_gift.html', {'form':form})

@login_required
def delete_gift(request, gift_id):
    gift = Gift.objects.get(pk=gift_id)
    gift.delete()
    gifts_posted_by_user = Gift.objects.filter(user=request.user)
    return render(request, 'gift/profile.html', {'user': request.user, 'gifts':gifts_posted_by_user})

# Profile views
@login_required
def view_profile(request, username):
    user = request.user
    profile = User.objects.get(username=username)
    gifts_posted_by_user = Gift.objects.filter(user=user)
    gifts_by_viewed_user = Gift.objects.filter(user=profile)
    return render(request, 'gift/profile.html', {
                                                    'user': user,
                                                    'profile': profile,
                                                    'gifts': gifts_posted_by_user,
                                                    'profile_gifts': gifts_by_viewed_user,
                                                })

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            if profile.avatar:
                file_type = profile.avatar.url.split('.')[-1]
                if file_type not in IMAGE_FILE_TYPES:
                    context = {
                        'profile_form': profile_form,
                        'user_form': user_form,
                        'error_message': 'Image file must be PNG, JPG, or JPEG',
                    }
                    return render(request, 'gift/edit_profile.html', context)
            profile.save()
            context = {
                'user': request.user,
                'profile': request.user,
                'gifts': Gift.objects.filter(user=request.user),
                'success_message': 'You succesfully updated your profile',
            }
            return render(request, 'gift/profile.html', context)
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
                'error_message': 'Error saving profile info',
            }
            return render(request, 'gift/edit_profile.html', context)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'gift/edit_profile.html', {'user_form': user_form,'profile_form': profile_form})

@login_required
def delete_user(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        return render(request, 'gift/delete.html', {'success_message': 'You succesfully deleted your account.'})
    except:
        error_message = 'Something went wrong.'
    return render(request, 'gift/delete.html', {'error_message': error_message})

# Authentication
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                gifts = Gift.objects.all().order_by('-id') # or filter by user
                return render(request, 'gift/index.html', {'gifts': gifts, 'user':user})
            else:
                return render(request, 'gift/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'gift/login.html', {'error_message': 'Invalid login'})
    return render(request, 'gift/login.html')

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account'
            message = render_to_string('gift/acc_active_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            # probably a good idea to make a template
            return HttpResponse('Please confirm your email to complete registration')
    else:
        form = SignupForm()
    return render(request, 'gift/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('/gifts/')
    else:
        return HttpResponse('Activation link is invalid!')

