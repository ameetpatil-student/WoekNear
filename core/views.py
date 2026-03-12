from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Usertype, Profile

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register2")

        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create a profile for the new user immediately
        # We use get_or_create to prevent "IntegrityError" if a signal already created it
        Profile.objects.get_or_create(user=user)

        messages.success(request, "Account created! Please login.")
        return redirect("employer_login")
    return render(request, "register2.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create a profile for the new user immediately
        # We use get_or_create to prevent "IntegrityError" if a signal already created it
        Profile.objects.get_or_create(user=user)

        messages.success(request, "Account created! Please login.")
        return redirect("login_view")
    return render(request, "register.html")


# 1. JOB SEEKER LOGIN VIEW
# ---------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        username_input = request.POST.get("username")
        password_input = request.POST.get("password")
        role_choice = request.POST.get("role_choice") 
        
        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            login(request, user)
            try:
                profile, created = Profile.objects.get_or_create(user=user)
                
                # Assign role if missing
                if not profile.usertype and role_choice:
                    db_role = "jobseeker" if role_choice == "seeker" else "employer"
                    role_obj, _ = Usertype.objects.get_or_create(type=db_role)
                    profile.usertype = role_obj
                    profile.save()
                
                # Redirect based on role
                if profile.usertype:
                    user_role = profile.usertype.type.lower()
                    if "jobseeker" in user_role:
                        return redirect("jobseeker_home")
                    elif "employer" in user_role:
                        return redirect("employer_home")
                
                return redirect("index") 
            except Exception as e:
                print(f"Redirect error: {e}")
                return redirect("index")
        else:
            messages.error(request, "Invalid username or password")

    # If it's a GET request, show the Seeker Login Page
    return render(request, "login.html")


def employer_login(request):
    if request.method == "POST":
        username_input = request.POST.get("username")
        password_input = request.POST.get("password")
        role_choice = request.POST.get("role_choice") 
        
        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            login(request, user)
            try:
                profile, created = Profile.objects.get_or_create(user=user)
                
                # Assign role if missing
                if not profile.usertype and role_choice:
                    db_role = "jobseeker" if role_choice == "seeker" else "employer"
                    role_obj, _ = Usertype.objects.get_or_create(type=db_role)
                    profile.usertype = role_obj
                    profile.save()
                
                # Redirect based on role
                if profile.usertype:
                    user_role = profile.usertype.type.lower()
                    if "jobseeker" in user_role:
                        return redirect("jobseeker_home")
                    elif "employer" in user_role:
                        return redirect("employer_home")
                
                return redirect("index") 
            except Exception as e:
                print(f"Redirect error: {e}")
                return redirect("index")
        else:
            messages.error(request, "Invalid username or password")

    # If it's a GET request, show the Employer Login Page
    return render(request, "login1.html")

# You must also define these two views so the server doesn't crash on the URLs
@login_required
def jobseeker_home(request):
    return render(request, "jobseeker_home.html")

@login_required
def employer_home(request):
    return render(request, "employer_home.html")


def logout_view(request):
    logout(request)
    # Changed from 'login' to 'login_view' to match your URL name
    return redirect("login_view")

def index(request):
    return render(request, "index.html")

# ADD THIS FOR FORGOT PASSWORD (Simple placeholder for now)
def forgot_password(request):
    if request.method == "POST":
        email_input = request.POST.get("email")
        
        # 1. Check if a user with this email exists in the database
        user = User.objects.filter(email=email_input).first()
        
        if user:
            # 2. If they exist, save their email securely in the session
            request.session['reset_email'] = email_input
            return redirect("reset_password") # Send them to the change password page
        else:
            # 3. If they don't exist, show an error
            messages.error(request, "No account found with that email address.")
            return redirect("forgot_password")
            
    return render(request, "forgot-password.html")



def reset_password(request):
    # Security check: Ensure they came from the forgot password page
    email = request.session.get('reset_email')
    if not email:
        return redirect("forgot_password")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            # Find the user and securely set the new password
            user = User.objects.get(email=email)
            user.set_password(new_password) # .set_password encrypts it securely!
            user.save()
            
            # Clear the session for security
            del request.session['reset_email']
            
            messages.success(request, "Password updated successfully! Please log in.")
            return redirect("login_view")
        else:
            messages.error(request, "Passwords do not match. Please try again.")

    return render(request, "reset_password.html")


def forgot_password1(request):
    if request.method == "POST":
        email_input = request.POST.get("email")
        
        # 1. Check if a user with this email exists in the database
        user = User.objects.filter(email=email_input).first()
        
        if user:
            # 2. If they exist, save their email securely in the session
            request.session['reset_email'] = email_input
            return redirect("reset_password") # Send them to the change password page
        else:
            # 3. If they don't exist, show an error
            messages.error(request, "No account found with that email address.")
            return redirect("forgot_password1")
            
    return render(request, "forgot-password1.html")



def reset_password1(request):
    # Security check: Ensure they came from the forgot password page
    email = request.session.get('reset_email')
    if not email:
        return redirect("forgot_password1")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            # Find the user and securely set the new password
            user = User.objects.get(email=email)
            user.set_password(new_password) # .set_password encrypts it securely!
            user.save()
            
            # Clear the session for security
            del request.session['reset_email']
            
            messages.success(request, "Password updated successfully! Please log in.")
            return redirect("employer_login")
        else:
            messages.error(request, "Passwords do not match. Please try again.")

    return render(request, "reset_password1.html")