from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import User_details

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