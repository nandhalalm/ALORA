from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,'index.html')

def register_view(request):
    if request.method == "POST":
        name=request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['cpassword']
        address=request.POST['address']
        gender=request.POST['gender']
        phonenumber=request.POST['phonenumber']

        if password1 != password2:
            context = {'error_message': 'Passwords do not match.'}
            return render(request, 'register.html', context)

        if User.objects.filter(username=username).exists():
            context = {'error_message': 'Username already exists.'}
            return render(request, 'register.html', context)

        if User.objects.filter(email=email).exists():
            context = {'error_message': 'Email already registered.'}
            return render(request, 'register.html', context)
        
        if User_details.objects.filter(phone_number=phonenumber).exists():
            context = {'error_message': 'phone number not match.'}
            return render(request, 'register.html', context)

        user = User.objects.create_user(first_name=name,username=username, email=email, password=password1)
        user.save()

        user_details = User_details.objects.create(user_id=user,gender=gender,phone_number=phonenumber,address=address)
        user_details.save()

        context = {'success_message': 'Account created successfully. Please log in.'}
        return render(request, 'login.html', context)

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        admin_user=authenticate(request,username=username,password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request,admin_user)
           # return redirect('admin:index')#admin
            return redirect('admin')

        if user is not None:
            login(request, user)
            return redirect(userhome) 
        else:
            context = {'error_message': 'Invalid username or password.'}
            return render(request, 'login.html', context)

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    context = {'success_message': 'You have been logged out successfully.'}
    return render(request, 'login.html', context)  


def userhome(request):
    return render(request,'userhome.html')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    user_details = User_details.objects.filter(user_id=request.user).first()  

    context = {'user': request.user, 'user_details': user_details}
    return render(request, 'profile.html', context)


def edit_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    user_details = User.objects.get(id=request.user.id)
    user = User_details.objects.get(user_id=user_details.id)

    if request.method == "POST":
        
        user.user_id.first_name=request.POST['name']
        user.user_id.email=request.POST['email']
        user.gender=request.POST['gender']
        user.address=request.POST['address']
        user.phone_number=request.POST['phone_number']
        user.save()
        return redirect(profile_view)

    context = {'user_details': user}
    return render(request, 'editprofile.html', context)

def delete_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    if request.method == "POST":
        user_details = User_details.objects.filter(user_id=request.user).first()  
        if user_details:
            user_details.delete()
        request.user.delete() 

        context = {'success_message': 'Your account has been deleted successfully.'}
        return render(request, 'login.html', context) 

    context = {'user': request.user}
    return render(request, 'delete_profile.html', context)


# admin...........................................

def admin(request):
   return render(request,'adminhome.html')

def viewusers(request):
 
    user_details = User_details.objects.all()
    context = {
        
        'user_details': user_details,
    }
    return  render(request,'viewusers.html',context)

def hall_details(request):
    data=Halls.objects.all()
    return render(request,'hall_details.html',{'data':data})

def add_hall(request):
    if request.method == 'POST':
        name=request.POST['hallname']
        location=request.POST['location']
        capacity=request.POST['capacity']
        price=request.POST['price']
        image=request.FILES['photo']
        description=request.POST['des']
        obj=Halls.objects.create(hall_name=name,location=location,capacity=capacity,price_per_day=price,photo_url=image,hall_description=description)
        obj.save()
        return redirect(hall_details)
    else:
        return render(request,'add_hall.html')
    
def food_details(request):
    data=Food.objects.all()
    return render(request,'food_details.html',{'data':data})


def add_food(request):
    if request.method == 'POST':
        name=request.POST['name']
        image=request.FILES['img']
        price=request.POST['price']
        obj=Food.objects.create(food_name=name,food_image=image,food_price=price)
        obj.save()
        return redirect(food_details)
    else:
        return render(request,'add_food.html')
    
 #PASSWORDS

def send_otp(email):
    otp = random.randint(100000, 999999)
    send_mail(
        'Your OTP Code',
        f'Your OTP code is: {otp}',
        'nandhalal608@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp

def password_reset_request(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = send_otp(email)
            context = {
                "email": email,
                "otp": otp,
                "message": "OTP has been sent to your email."
            }
            return render(request, 'forgot_password2.html', context)
        except User.DoesNotExist:
            context["error"] = "Email address not found."
    return render(request, 'forgot_password1.html', context)

def verify_otp(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        otpold = request.POST.get('otp1')
        otp = request.POST.get('otp2')

        if otpold == otp:
            context = {
                'otp': otp,
                'email': email,
                "message": "OTP verified successfully."
            }
            return render(request, 'forgot_password3.html', context)
        else:
            context = {
                "email": email,
                "error": "Invalid OTP. Please try again."
            }
    return render(request, 'forgot_password2.html', context)

def set_new_password(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                context["success"] = "Password has been reset successfully. Please log in."
                return redirect(profile_view)
            except User.DoesNotExist:
                context["error"] = "User does not exist."
        else:
            context = {
                "email": email,
                "error": "Passwords do not match. Please try again."
            }
    context["email"] = email
    return render(request, 'forgot_password3.html', context)

#decorations

def decoration_details(request):
    data=Decoration.objects.all()
    return render(request,'decoration_details.html',{'data':data})
def add_decoration(request):
    if request.method == 'POST':
        name=request.POST['name']
        price=request.POST['price']
        image=request.FILES['image']
        obj=Decoration.objects.create(decoration_name=name,decoration_price=price,decoration_image=image)
        obj.save()
        return redirect(decoration_details)
    return render(request,'add_decoration.html')

#BOOKINGS................................................................

@login_required(login_url='login')
def booking_page(request):
    halls=Halls.objects.all()
    foods=Food.objects.all()
    decorations=Decoration.objects.all()
    photography_price=5000

    if request.method == 'POST':
        event_date=request.POST['event_date']
        hall_id=request.POST['hall']
        food_id=request.POST.get('food')                #paranthesis bcz it's optional
        decoration_id=request.POST.get('decoration')
        photography=request.POST.get('photography')
        no_of_persons=int(request.POST['no_of_persons'])

        hall=Halls.objects.get(id=hall_id)
        food=Food.objects.get(id=food_id)if food_id else None                           #fetch hall,food and decoration object
        decoration=Decoration.objects.get(id=decoration_id)if decoration_id else None

        total_cost=0
        total_cost=hall.price_per_day
        if food:
            total_cost +=food.food_price*no_of_persons

        if decoration:                                                      #Calculation of total price
            total_cost +=decoration.decoration_price*no_of_persons
        
        if photography=='yes':
            total_cost +=photography_price

        booking=Bookings.objects.create(event_date=event_date,user_id=request.user,hall_id=hall,food=food,
            decoration=decoration,
            photography_cost=photography_price if photography == 'yes' else 0,
            no_of_persons=no_of_persons,
            total_payment=total_cost,
            payment_status="pending",
        )

        booking.save()
        return redirect('booking_view')
    
    context = {'halls':halls,'foods':foods,'decorations':decorations,'photography_price':photography_price}
    return render(request,'booking_page.html',context)


@login_required(login_url='login')
def booking_view(request):
    booking = Bookings.objects.filter(user_id=request.user).order_by('-id').first()
    
    if not booking:
        messages.error(request, "No booking found.")
        return redirect('booking_page')

    context = {
        'booking': booking
    }
    return render(request, 'booking_view.html', context)