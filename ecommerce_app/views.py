from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product,Orders,OrderUpdate
from math import ceil
from django import forms
from users_app.models import Newsletter
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from users_app.models import Profile
import json
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from django.views.decorators.cache import cache_page
from .forms import EditProfileSupport

from django.contrib.sites.shortcuts import get_current_site
import ast

from django.core.paginator import Paginator



razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
class NewsletterSupport(forms.ModelForm):
    class Meta:
        model=Newsletter
        fields="__all__"

@login_required(login_url="signin1")
def Home(request):

    if cache.get("products"):
        print("products from cache")
        allProds=cache.get("products")
    
    else:

        allProds=[]
        category_filter=Product.objects.values('category')
        cats={item['category'] for item in category_filter}

        for cat in cats:
            prods=Product.objects.filter(category=cat)
            n=len(prods)
            nSlides=n//4 + ceil((n/4) - n//4)
            allProds.append([prods,range(1,nSlides),nSlides])

        
        cache.set("products",allProds,3600)
        print("products from database")
    
    return render(request,"home.html",{'allProds': allProds})


@login_required(login_url="signin1")
def Checkout1(request):
    return render(request,"checkout1.html")
    

@login_required(login_url="signin1")    
def Address(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json,name=name,amount=int(amount), email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        
        Order.save()

        DATA = {
            "amount": int(amount)*100,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "name": name,
                "email": email,
                "phone":phone,
                "order_id":Order.id, #from Orders table
            }
        }

        razorpay_order=razorpay_client.order.create(data=DATA)
        razorpay_order_id = razorpay_order['id']
        update = OrderUpdate(orders_id=Order.id,amount=amount,email=email,updated_order_id=razorpay_order_id,update_desc="the order has been placed")
        update.save()

        """--------------------------------------------"""
        callback_url = f"{get_current_site(request)}/paymenthandler/"
        print(callback_url)

        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = 'INR'
        context['callback_url'] = callback_url
        context['cust_name']=name
        context['email']=email
        context['contact']=phone
 
        return render(request, 'payment1.html', context=context)
    else:

        profile=request.user.profile
        return render(request,"address.html",{'profile':profile})
    

def About(request):
    return render(request,'about.html')

@login_required(login_url="signin1")
def Profile_Page(request):

    
    profile=f"{request.user.profile}_profile"
    order=f"{request.user.email}_order"
    

    if cache.get(profile):
        profile1=cache.get(profile)
        print("profile from Cache")
    else:
        profile1=request.user.profile
        cache.set(profile,profile1,timeout=3600)
        print("profile from Database")

    if cache.get(order):
        print("order from cache")
        order_details=cache.get(order)
    else:
        order_details=Orders.objects.filter(email=request.user.email)
        print("order from database")
        cache.set(order,order_details,timeout=3600)
    
    """profile1=request.user.profile
    order_details=Orders.objects.filter(email=request.user.email)"""

    paginator=Paginator(order_details,5)

    page_number=request.GET.get('page')

    page_obj=paginator.get_page(page_number)



    return render(request,'profile.html',{'profile1':profile1,'order1':page_obj})


@login_required(login_url="signin1")
def Order_details(request,pk):
    ord_det=Orders.objects.get(id=pk)

    string_dict=ord_det.items_json
    json_object = json.loads(string_dict)

    key_value_pairs = []
    for key, value in json_object.items():
        key_value_pairs.append((key, value))

    dict_items = dict(key_value_pairs)



    upd_det=OrderUpdate.objects.get(orders_id=pk)
   
    return render(request,'order_details.html',{'order1':ord_det,'update1':upd_det,'dict_items':dict_items})



@login_required(login_url="signin1")
def EditProfile(request):

    if request.method=="POST":

        form=EditProfileSupport(request.POST,request.FILES,instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.info(request,"Profile updated successfully!")
            return redirect('profile1')
        
        else:
            print(form.errors)
            messages.warning(request,"Some error occured!")
            form=EditProfileSupport(instance=request.user.profile)
            print("error occurred")

            return render(request,'edit_profile.html',{'form':form})


    else:

        instance1=request.user.profile
        form=EditProfileSupport(instance=instance1)
        return render(request,'edit_profile.html',{'form':form})
    

@login_required(login_url="signin1")    
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
           
            # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }


        try:
            updated_order=OrderUpdate.objects.get(updated_order_id=razorpay_order_id)
            updated_order.payment_id=payment_id

        except:
            context={
                'order_id':razorpay_order_id,
            }

            return render(request, 'paymentfail.html',context=context)
        
        else:


            try:
            

                razorpay_client.utility.verify_payment_signature(params_dict)
                updated_order.payment_status="success"
                updated_order.save()
                context={
                    'order_id':razorpay_order_id,
                    'payment_id':payment_id,
                }
                return render(request, 'paymentsuccess.html',context=context)
        
            except razorpay.errors.SignatureVerificationError as e:
                updated_order.payment_status="failure"
                updated_order.save()
                context={
                    'order_id':razorpay_order_id,
                }
                return render(request, 'paymentfail.html',context=context)
 


