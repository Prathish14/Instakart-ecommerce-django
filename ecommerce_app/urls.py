from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.Home,name="home1"),
    path('about/',views.About,name="about1"),
    path('profile/',views.Profile_Page,name="profile1"),
    path('edit-profile/',views.EditProfile,name="edit1"),
    path('order-details/<str:pk>',views.Order_details,name="ord_det1"),
    path('checkout1/',views.Checkout1,name="checkout1"),
    path('address/',views.Address,name="address1"),
    path('paymenthandler/', views.paymenthandler, name='handler1'),


] 

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)