from django.contrib.auth import get_user_model, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import User
from .forms import UserCreationForm, AlmostDoneForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .token import generate_token
from django.core.mail import send_mail
from StackOverFlowClone.settings import EMAIL_HOST_USER


# Create your views here.
def index(request):
    logout(request)
    return HttpResponse('Home Page')


def profile(request, user_id):
    user_data = User.objects.get(pk=user_id)
    return HttpResponse(user_data.profile_picture)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('user:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user:index')
        else:
            try:
                user = User.objects.get(email=request.POST.get('username'))
            except User.DoesNotExist:
                user = None

            if user is not None and not user.is_active and user.check_password(request.POST.get('password')):
                return render(request, 'user/check-mail.html', {
                    'email': request.POST.get('username')
                })
            return render(request, 'user/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'user/login.html', {'form':form})


def signup(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'profile_pic' in request.FILES:
                request.FILES['profile_pic'].name = f"pp_{request.user.id}.png"
            form = AlmostDoneForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('user:signup')
        if request.user.name == '' and request.user.profile_pic == 'profile_pictures/default.png':
            form = AlmostDoneForm(instance=request.user)
            return render(request, 'user/almost-done.html', {
                'form': form,
                'email': request.user.email,
                'picture': request.user.profile_pic.url
            })
        return redirect('user:index')
    if request.method == 'POST':
        email = request.POST.get('email')
        MyUser = get_user_model()

        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            user = None

        if user is not None:
            if not user.is_active:
                return render(request, 'user/check-mail.html', {'email': email})
            login(request, user)
            return redirect('user:signup')

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(subject=mail_subject, message="", from_email=EMAIL_HOST_USER , recipient_list=[to_email],
                      html_message=message)
            return render(request, 'user/check-mail.html', {'email': to_email})
    else:
        form = UserCreationForm()
    return render(request, 'user/signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('user:signup')
    else:
        return HttpResponse('Invalid')
