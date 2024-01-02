from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str

from .tokens import account_activation_token

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import get_template

from ecommerce_app.views import NewsletterSupport




from django import forms

from .models import Contact,Newsletter

# Create your views here.

class SupportToSignup(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password1','password2']

def Signup(request):

    if request.method=="POST":
        form=SupportToSignup(request.POST)

        if request.POST.get('password1') != request.POST.get('password2'):
            messages.error(request,"Your passwords doesn't mach!!! ")
            return render(request,"signup.html",{'form':form})
        
        try:
            if User.objects.get(email=request.POST.get('email')):
                pass
        except:
            pass
        else:
            messages.error(request,"Account with email alredy exist!!!")
            return render(request,"signup.html",{'form':form})


        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            # Send email confirmation
            current_site = get_current_site(request)
            subject1 = 'Activate your instakart account'
            """message = render_to_string('activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            
            email = EmailMessage(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        )
            
            email.send()"""

            context={
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                }
            
            message = get_template("activate.html").render(context)
            mail = EmailMessage(
            subject=subject1,
            body=message,
            from_email="prathishgm14@gmail.com",
            to=[user.email],
            reply_to=["prathishgm14@gmail.com"],
            )
            mail.content_subtype = "html"
            mail.mixed_subtype = 'related'
            mail.send()
            
            return redirect("activate_mail_sent1")
           
        else:
            messages.error(request,"Oops some error occured!!!")
            return render(request,"signup.html",{'form':form})

        
    else:
        form=SupportToSignup()
        return render(request,"signup.html",{'form':form})
    

def ActivateMailSent(request):
    return render(request,"activate_mail_sent.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        context={}
        message = get_template("signup_success.html").render(context)
        mail = EmailMessage(
        subject="Account Created Successfully",
        body=message,
        from_email="prathishgm14@gmail.com",
        to=[user.email],
        reply_to=["prathishgm14@gmail.com"],
        )
        mail.content_subtype = "html"
        mail.mixed_subtype = 'related'
        mail.send()

        messages.success(request,"Your Account activated successfully!!!")
        return redirect('activate_success1')
    
    
    else:
        messages.warning(request,"This token is not valid!!!")
        return redirect("signup1")
    
def Activate_Success(request):
    
    return render(request,"activate_success.html")

@login_required(login_url="signin1")
def SignOut(request):
    logout(request)
    messages.info(request,"You have now signed out !!!")
    return redirect("signin1")

def SignIn(request):
    if request.method=="POST":
        form=AuthenticationForm(request.POST)

    
        try:
            if User.objects.get(username=request.POST.get('username')):
                pass
        except:
            messages.error(request,"Username doesn't exist!!!")
            return render(request,"signin.html",{'form':form})
        
        user=authenticate(username=request.POST.get('username'),password=request.POST.get('password'))


        if user:
            login(request,user)
            messages.info(request,"You have now successfully signed in !!!")
            return redirect("home1")
        else:
            form=AuthenticationForm()
            messages.error(request,"Your Password is wrong !!!")
            return render(request,"signin.html",{'form':form})
    else:

        form=AuthenticationForm()
        return render(request,"signin.html",{'form':form})
    

class Contact_Support(forms.ModelForm):
    class Meta:
        model=Contact
        fields="__all__"


def ContactUs(request):

    if request.method=="POST":

        if 'newsletter1' in request.POST:
            form=NewsletterSupport(request.POST)
            email1=request.POST.get('email')

            try:
                if Newsletter.objects.get(email=email1):
                    pass
            except:
                if form.is_valid():
                    form.save()
                    messages.info(request,"Email Submitted Successfully!!!")
                    return redirect("contact1")
            else:
                messages.warning(request,"This Email alredy registerd for newsletter!!!")
                return redirect("contact1")  
            
        elif 'contact123' in request.POST:
            form=Contact_Support(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request,"Query sent successsfully...")
                return redirect('contact1')
            else:
                messages.error(request,"Some error occured!!!")
                return render(request,"contact.html")

        
    
    else:
        return render(request,"contact.html")
