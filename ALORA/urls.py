"""ALORA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views
   
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('',views.index,name='index'),  
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),

    path('userhome/',views.userhome,name='userhome'), 
    path('profile/', views.profile_view, name='profile'),  
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),  
    path('delete-profile/', views.delete_profile_view, name='delete_profile'),


    path('admin', views.admin, name='admin'), 
    path('viewusers',views.viewusers,name='viewusers'),
    path('addhall',views.add_hall,name='addhall'),
    path('adddetails',views.hall_details,name='halldetails'),
    path('addfood',views.add_food,name='addfood'),
    path('fooddetails',views.food_details,name='fooddetails'),

    path('resetpassword',views.password_reset_request,name='resetpassword'),
    path('verifyotp',views.verify_otp,name='verifyotp'),
    path('newpassword',views.set_new_password,name='newpassword'),

    path('adddecoration',views.add_decoration,name='adddecoration'),
    path('decorationdetails',views.decoration_details,name='decorationdetails'),

    path('booking_page',views.booking_page,name='booking_page'),
    path('booking_view',views.booking_view,name='booking_view'),
    path('admin_view_booking',views.admin_view_booking,name='admin_view_booking'),
    path('acceptrejectbooking/<int:id>',views.accept_reject_booking,name='acceptrejectbooking'),
    path('payment',views.stripe_payments,name='payment'),
]
if settings.DEBUG:
    
   urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)