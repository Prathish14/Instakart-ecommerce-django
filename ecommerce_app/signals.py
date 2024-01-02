from .models import OrderUpdate,Orders,Product
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.template.loader import get_template
from django.core.mail import EmailMessage

from users_app.models import Profile

from django.core.cache import cache
from math import ceil

import ast

dict1={'id'}


@receiver(post_save,sender=Orders)
def Order_items_info_mail(sender, instance, created, **kwargs):
    if created:

        items=ast.literal_eval(instance.items_json)

        context={'name':instance.name, 'list': items, 'amount': instance.amount}

        message = get_template("order_summary_mail.html").render(context)
        mail = EmailMessage(
        subject="Order Summary",
        body=message,
        from_email="prathishgm14@gmail.com",
        to=[instance.email],
        reply_to=["prathishgm14@gmail.com"],
        )
        mail.content_subtype = "html"
        mail.mixed_subtype = 'related'
        mail.send()





@receiver(post_save,sender=OrderUpdate)
def Order_succ_mail(sender, instance, created, **kwargs):
    if instance.delivered == True:
        context={'order_id':instance.updated_order_id,'payment_id':instance.payment_id,'amount':instance.amount}

        message = get_template("delivery_succ_mail.html").render(context)
        mail = EmailMessage(
        subject="Your Order Has Been Successfully Delivered!",
        body=message,
        from_email="prathishgm14@gmail.com",
        to=[instance.email],
        reply_to=["prathishgm14@gmail.com"],
        )
        mail.content_subtype = "html"
        mail.mixed_subtype = 'related'
        mail.send()

        

    
    if instance.payment_status == "success":

        if instance.updated_order_id not in dict1:

            dict1.add(instance.updated_order_id)

            context={'payment_id':instance.payment_id,'order_id':instance.updated_order_id,'status':instance.payment_status}

            message = get_template("order_succ_mail.html").render(context)
            mail = EmailMessage(
            subject="Your Order Placed Successfully!",
            body=message,
            from_email="prathishgm14@gmail.com",
            to=[instance.email],
            reply_to=["prathishgm14@gmail.com"],
            )
            mail.content_subtype = "html"
            mail.mixed_subtype = 'related'
            mail.send()



        

    elif instance.payment_status == "failure":

        if instance.updated_order_id not in dict1:
            dict1.add(instance.updated_order_id)


            context={'order_id':instance.updated_order_id,'status':instance.payment_status}

            message = get_template("order_succ_mail.html").render(context)
            mail = EmailMessage(
            subject="Your Payment failed !",
            body=message,
            from_email="prathishgm14@gmail.com",
            to=[instance.email],
            reply_to=["prathishgm14@gmail.com"],
            )
            mail.content_subtype = "html"
            mail.mixed_subtype = 'related'
            mail.send()




@receiver(post_save,sender=Profile)
def Update_profile_cache(sender, instance, created, **kwargs):
    print("Profile cache update triggerd")
    cache.set(f"{instance}_profile",instance,3600)


@receiver(post_save,sender=Orders)
def Update_order_cache(sender, instance, created, **kwargs):
    print("Orders cache update triggerd")
    print(instance,instance.email)
    cache.set(f"{instance.email}_order",Orders.objects.filter(email=instance.email),3600)


@receiver(post_save,sender=Product)
def Update_product_cache(sender, instance, created, **kwargs):
    print("Produt cache update triggerd")

    allProds=[]
    category_filter=Product.objects.values('category')
    cats={item['category'] for item in category_filter}

    for cat in cats:
        prods=Product.objects.filter(category=cat)
        n=len(prods)
        nSlides=n//4 + ceil((n/4) - n//4)
        allProds.append([prods,range(1,nSlides),nSlides])

    cache.set("products",allProds,3600)


