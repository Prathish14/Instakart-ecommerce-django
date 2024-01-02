from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Newsletter,Contact,Profile
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.contrib.auth.models import User
from ecommerce_app.models import OrderUpdate

from django.core.cache import cache

@receiver(post_save,sender=User)
def Profile_creation_signal(sender, instance, created, **kwargs):
    instance1=instance
    if created:
        pro_ref=Profile.objects.create(
            user=instance1,
            email=instance1.email,
        )


"""@receiver(post_save,sender=Profile)
def Cache_Update_Profile(sender, instance, created, **kwargs):
    profile=f"{instance}_profile"
    if cache.get(profile):
        print("cache updated!!!")
        cache.set(profile,instance,timeout=3600)
        print(instance)
    """



@receiver(post_save,sender=Contact)
def Contact_confirm_mail(sender, instance, created, **kwargs):
    if created:
        context={'name':instance.name,'id':instance.id}
        message = get_template("contact_query_recived.html").render(context)
        mail = EmailMessage(
        subject="Your Ticket/Query Recived!",
        body=message,
        from_email="prathishgm14@gmail.com",
        to=[instance.email],
        reply_to=["prathishgm14@gmail.com"],
        )
        mail.content_subtype = "html"
        mail.mixed_subtype = 'related'
        mail.send()

        print(sender, instance, created)



@receiver(post_save,sender=Newsletter)
def Newsletter_sub_succ_mail(sender, instance, created, **kwargs):
    if created:
        context={}
        message = get_template("newsletter.html").render(context)
        mail = EmailMessage(
        subject="Newsletter Subscription successfull!!!",
        body=message,
        from_email="prathishgm14@gmail.com",
        to=[instance.email],
        reply_to=["prathishgm14@gmail.com"],
        )
        mail.content_subtype = "html"
        mail.mixed_subtype = 'related'
        mail.send()

