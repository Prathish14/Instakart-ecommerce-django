from django.db import models

# Create your models here.

class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50,default="")
    sub_category=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=150)
    image=models.ImageField()

    def __str__(self):
        return self.product_name
    

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    items_json =  models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.EmailField(max_length=50)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)    
    phone = models.CharField(max_length=100,default="")

    def __str__(self):
        return self.name
    

class OrderUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    orders_id=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    updated_order_id=models.CharField(max_length=100,blank=True,null=True)
    payment_id = models.CharField(max_length=100,blank=True,null=True)
    amount=models.IntegerField(blank=True,null=True)
    choice=(
        ('success','success'),
        ('failure','failure'),
        ('na','na')
    )
    payment_status=models.CharField(max_length=20,choices=choice,default="na")
    update_desc = models.CharField(max_length=5000,blank=True,null=True)
    delivered=models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email


    

