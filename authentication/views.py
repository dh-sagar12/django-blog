
import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings
import secrets
from .models import Token
from django.shortcuts import get_object_or_404


from authentication.forms import UserCreationForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from authentication.models import  User

# Create your views here.

def LoginView(request):
    redirect_url =  request.GET.get('ReturnUrl')
    if request.user.is_authenticated:

        if redirect_url is None:
            return redirect(reverse('home'))
        else:
            return redirect(redirect_url)

    else:
        if request.method== 'POST':
            email=  request.POST.get('email')
            password=  request.POST.get('password')
            usr = User.objects.filter(email=email).first()
            redirect_url  =  request.POST.get('ReturnUrl')
            print(redirect_url)
            if usr:
                if usr.is_active:
                    authUser= authenticate(email= usr.email, password=password)
                    if authUser:
                        django_login(request, authUser)
                        if redirect_url is None:
                            return redirect(reverse('home'))
                        else:
                            return redirect(redirect_url)
                    else:
                        messages.error(request, 'Invalid Credentials' )
                        return render(request, 'authentication/login.html')

                else:
                    messages.error(request, 'Inactive account')
                    return render(request, 'authentication/login.html')
                        
                    
            else:
                messages.error(request, 'Invalid Credentials' )
                return render(request, 'authentication/login.html')
            
    return render(request, 'authentication/login.html')



def LogoutView(request):
    django_logout(request)
    return redirect(reverse('login'))


    
def invalid_multiple_token(request, user):
    tokens = Token.objects.filter(user_id=user, expired= False)
    for token in tokens:
        token.expired = True
        token.save()


def SendForgetPasswordEmail(request):
    if request.method == 'POST':
        email =  request.POST.get('email')
        try:
            user =  User.objects.get(email=email)
        except:
            messages.error(request, 'User Not found')
            return render(request, 'authentication/forgetpassword.html')
        if  user is not None:
            invalid_multiple_token(request, user)
            token =  secrets.token_urlsafe(20)
            print(token)
            token_instance = Token.objects.create(token=token, user_id= user)
            token_instance.save()
            base_url  =  get_current_site(request)
            link  =  f'http://{base_url}/auth/password/reset/{token}/'
            message  =  render_to_string('mail/forget_password_mail.html', {
                'user': user, 
                'link': link 
            })
            email  = EmailMessage('Change Your Password', message, settings.EMAIL_HOST_USER, [user.email])
            email.fail_silently  =  True
            email.content_subtype  = 'html'
            email.send()
            context  =  {
                'token_sent': True,
            }
            return render(request, 'authentication/forgetpassword.html', context=context)
    return render(request, 'authentication/forgetpassword.html')


def ResetPassword(request, token):
    try:
        token =  get_object_or_404(Token, token=  token, expired =  False)
    except Exception as e:
        messages.error(request, 'Invalid or Expired Token')
        return redirect(reverse('forgotPassword'))
    
    duration = datetime.datetime.now(datetime.timezone.utc) - token.created_on

    if duration.seconds >= 600:
        token.expired = True
        token.save()
        messages.error(request, 'Invalid or Expired Token')
        return redirect(reverse('forgotPassword'))

    if request.method  == 'POST':
        password1 =  request.POST.get('password1')
        password2 =  request.POST.get('password2')
        if password1 == password2:
            print(token.user_id)
            user  =  User.objects.get(id =  token.user_id.id)
            user.set_password(password1)
            user.save()
            invalid_multiple_token(request, user)
            messages.success(request, 'Password has been changed successfully!!')
            return redirect(reverse('login'))
        
        messages.error(request, "Password Didn't Matched")



    return render(request, 'authentication/set_password.html', {'token': token})




def SignUp(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    else:
        form = UserCreationForm()
        params = {'form': form}
        
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                email = request.POST.get('email')
                password = request.POST.get('password1')
                user = User.objects.get(email=email)
                print(user.email)
                authUser= authenticate(email= user.email, password=password)
                django_login(request, authUser)
                messages.error(request, 'Sign Up Successfully')
                return redirect(reverse('home'))
            else:
                return render(request, 'authentication/signup.html', {'form': form})
            
        return render(request, 'authentication/signup.html', params )


@login_required(login_url='/auth/login/', redirect_field_name='ReturnUrl')
def EditProfile(request):
    try:
        user_data = get_object_or_404(User, id=request.user.id)
        if request.method == 'GET':
            context = {
                'form': EditProfileForm(instance=user_data),
                'id': id,
                'form_title': 'Edit Profile',
                'author': user_data

            }

        elif request.method == 'POST':
            form = EditProfileForm(request.POST or None,request.FILES or None, instance=user_data)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Updated Successfully!!')
                return redirect(reverse('home'))
            else:
                context = {
                    'form': EditProfileForm(instance=user_data),
                    'id': id,
                    'form_title': 'Edit Profile',
                    'author': user_data


                }
    except Exception as e:
        messages.error(message="Invalid User", request=request)
        return redirect(reverse('home'))
    
    return render(request, 'authentication/edit_profile.html', context)
    

