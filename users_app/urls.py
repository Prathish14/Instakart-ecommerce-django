from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.Signup,name="signup1"),
    path('activate_mail/',views.ActivateMailSent,name="activate_mail_sent1"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activate_success/',views.Activate_Success,name="activate_success1"),
    path("signout/",views.SignOut,name="signout1"),
    path('signin/',views.SignIn,name="signin1"),

    #email - password reset
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name ='password_reset_complete'),


    path('contact_us/',views.ContactUs,name="contact1"),


]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
