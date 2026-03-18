from urllib import request

from django.contrib.auth.models import User 
from .models import StoreProfile , adminlogin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random




 # Make sure this matches your actual model name
@login_required 
def jobseeker_home(request):
    """View for the Job Seeker dashboard."""
    jobs_list = Job.objects.all() 
    context = {
        'jobs': jobs_list
    }
    return render(request, 'jobseeker_home.html', context)


@login_required 
def employer_dashboard(request):
    """View for the Employer dashboard."""
    return render(request, 'employer_dashboard.html')

# The @login_required decorator forces users to log in before seeing this page.
# If they are not logged in, Django will redirect them to your login URL.
@login_required 
def employer_dashboard(request):
    # This renders the HTML page. Because 'request' is passed in, 
    # the template automatically has access to the user's data.
    return render(request, 'employer_dashboard.html')

# Assuming these are in your models.py
from .models import Profile, Usertype 

# --- JOB SEEKER REGISTRATION ---
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password") 

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.get_or_create(user=user)

        messages.success(request, "Account created! Please login.")
        return redirect("login_view")
        
    return render(request, "register.html")

# --- EMPLOYER REGISTRATION ---
def employer_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password") 

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect("employer_register")
            
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("employer_register")

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.get_or_create(user=user)

        messages.success(request, "Employer Account created! Please login.")
        return redirect("employer_login")
        
    return render(request, "register2.html")


# --- JOB SEEKER LOGIN ---
def login_view(request):
    if request.method == "POST":
        email_input = request.POST.get("email") 
        password_input = request.POST.get("password")
        role_choice = request.POST.get("role_choice") 
        
        user = None
        
        try:
            user_obj = User.objects.get(email=email_input)
            user = authenticate(request, username=user_obj.username, password=password_input)
        except User.DoesNotExist:
            pass

        if user is not None:
            login(request, user)
            try:
                profile, created = Profile.objects.get_or_create(user=user)
                
                if not profile.usertype and role_choice:
                    db_role = "jobseeker" if role_choice == "seeker" else "employer"
                    role_obj, _ = Usertype.objects.get_or_create(type=db_role)
                    profile.usertype = role_obj
                    profile.save()
                
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
            messages.error(request, "Invalid email or password")

    return render(request, "login.html")


# --- EMPLOYER LOGIN ---
# --- EMPLOYER LOGIN ---
def employer_login(request):
    if request.method == "POST":
        # Check if the HTML form is sending an "email" OR a "username"
        login_input = request.POST.get("email") or request.POST.get("username")
        password_input = request.POST.get("password")
        role_choice = request.POST.get("role_choice") 
        
        user = None
        
        # Try to authenticate. If there's an '@', treat it as an email lookup first.
        if login_input and '@' in login_input:
            try:
                user_obj = User.objects.get(email=login_input)
                user = authenticate(request, username=user_obj.username, password=password_input)
            except User.DoesNotExist:
                pass
        else:
            # Otherwise, treat it as a standard username
            user = authenticate(request, username=login_input, password=password_input)

        if user is not None:
            login(request, user)
            try:
                profile, created = Profile.objects.get_or_create(user=user)
                
                if not profile.usertype and role_choice:
                    db_role = "jobseeker" if role_choice == "seeker" else "employer"
                    role_obj, _ = Usertype.objects.get_or_create(type=db_role)
                    profile.usertype = role_obj
                    profile.save()
                
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

    return render(request, "login1.html")


# --- HOME PAGES ---

@login_required
def employer_home(request):
    return render(request, "employer_home.html")

def index(request):
    return render(request, "index.html")

def logout_view(request):
    logout(request)
    return redirect("login_view")


# --- JOB SEEKER PASSWORD RESET ---
def forgot_password(request):
    if request.method == "POST":
        email_input = request.POST.get("email")
        user = User.objects.filter(email=email_input).first()
        
        if user:
            request.session['reset_email'] = email_input
            return redirect("reset_password") 
        else:
            messages.error(request, "No account found with that email address.")
            return redirect("forgot_password")
            
    return render(request, "forgot-password.html")

def reset_password(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect("forgot_password")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            user = User.objects.get(email=email)
            user.set_password(new_password) 
            user.save()
            del request.session['reset_email']
            
            messages.success(request, "Password updated successfully! Please log in.")
            return redirect("login_view")
        else:
            messages.error(request, "Passwords do not match. Please try again.")

    return render(request, "reset_password.html")


#EMPLOYER PASSWORD RESET 
def forgot_password1(request):
    if request.method == "POST":
        email_input = request.POST.get("email")
        user = User.objects.filter(email=email_input).first()
        
        if user:
            request.session['reset_email'] = email_input
            # FIX 1: Change this to reset_password1
            return redirect("reset_password1") 
        else:
            messages.error(request, "No account found with that email address.")
            # FIX 2: Make sure this points to forgot_password1
            return redirect("forgot_password1")
            
    return render(request, "forgot-password1.html")

def reset_password1(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect("forgot_password1")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            user = User.objects.get(email=email)
            user.set_password(new_password) 
            user.save()
            
            del request.session['reset_email']
            
            messages.success(request, "Password updated successfully! Please log in.")
            # This ensures they go to the employer login after resetting!
            return redirect("employer_login")
        else:
            messages.error(request, "Passwords do not match. Please try again.")

    return render(request, "reset_password1.html")

# MISC VIEWS 
def add_adds(request):
    return render(request, "add_adds.html")



# user profile 
@login_required
def register_store_profile(request):
    if request.method == 'POST':
        # 1. Pull all text data manually from the HTML form's "name" attributes
        name = request.POST.get('name')
        email = request.POST.get('email')
        store_name = request.POST.get('store_name')
        
        # --- NEW FIELDS CAPTURED HERE ---
        category = request.POST.get('category')             
        description = request.POST.get('description')       
        # --------------------------------
        
        store_location = request.POST.get('store_location')
        mobile_number = request.POST.get('mobile_number')
        
        # 2. Pull the uploaded file from request.FILES
        verification_document = request.FILES.get('verification_document')

        # 3. Get the existing profile for this user, or create a blank new one
        # Change 'user' to 'employer'
        profile, created = StoreProfile.objects.get_or_create(employer=request.user)
        
        # 4. Map the HTML data to the database columns
        profile.name = name
        profile.email = email
        profile.store_name = store_name
        
        # --- NEW FIELDS SAVED HERE ---
        profile.category = category             
        profile.description = description       
        # -----------------------------
        
        profile.store_location = store_location
        profile.mobile_number = mobile_number
        
        # Only overwrite the document if they actually uploaded a new one
        if verification_document:
            profile.verification_document = verification_document
            
        # 5. Save the final profile to the database
        profile.save()

        # 6. Redirect them back to their dashboard
        # Make sure 'employer_home' matches the name=... in your urls.py file
        return redirect('employer_home') 

    # If it's a GET request (they just clicked a link to get here), show the form
    return render(request, 'store_registration.html')


@login_required(login_url='login_view') 
def employer_home(request):
    context = {
        'has_profile': False,
        'is_approved': False,
    }
    try:
        profile = StoreProfile.objects.get(employer=request.user)
        context['has_profile'] = True
        context['is_approved'] = profile.is_approved # This must be True after you click Approve
    except StoreProfile.DoesNotExist:
        pass

    return render(request, 'employer_home.html', context)
#admin login
def register_view(request):
    context = {}
    
    if request.method == 'POST':
        # --- PHASE 1: User clicks "Register & Send OTP" ---
        if 'send_otp' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            # Check if passwords match
            if password != confirm_password:
                context['error'] = "Passwords do not match!"
                return render(request, 'admin_register.html', context) # Update template name if needed
                
            # Check if username already exists
            if adminlogin.objects.filter(username=username).exists():
                context['error'] = "Username already exists!"
                return render(request, 'admin_register.html', context)

            # Generate OTP and store details in session
            otp = str(random.randint(1000, 9999))
            request.session['temp_username'] = username
            request.session['temp_password'] = password
            request.session['otp'] = otp
            
            # Send the email
            subject = 'Admin Registration OTP'
            message = f'Your Admin Registration OTP is: {otp}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, ['ameetpatil122@gmail.com'])
            
            # Tell HTML to show the OTP field and show a success message
            context['otp_sent'] = True
            context['success'] = "OTP has been sent to ameetpatil122@gmail.com."
            return render(request, 'admin_register.html', context)
            
        # --- PHASE 2: User clicks "Verify & Create Account" ---
        elif 'verify_otp' in request.POST:
            entered_otp = request.POST.get('otp')
            actual_otp = request.session.get('otp')
            
            # If OTP matches successfully
            if entered_otp == actual_otp:
                # Save to database
                username = request.session.get('temp_username')
                password = request.session.get('temp_password')
                new_admin = adminlogin(username=username, password=password)
                new_admin.save()
                
                # Clear session data
                del request.session['temp_username']
                del request.session['temp_password']
                del request.session['otp']
                
                # REDIRECT to Admin Login Page upon success
                return redirect('admin_login_view') 
                
            # If OTP is wrong
            else:
                context['otp_sent'] = True # Keep the OTP field visible
                context['error'] = 'Invalid OTP. Please try again.' # Show error message
                return render(request, 'admin_register.html', context)

    return render(request, 'admin_register.html', context)

def admin_login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        
        # Check if a record exists with this exact username and password
        admin_exists = adminlogin.objects.filter(username=uname, password=pword).exists()
        
        if admin_exists:
            request.session['admin_logged_in'] = True
            return redirect('admin_home_view')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid Credentials'})
            
    return render(request, 'admin_login.html')

def admin_home_view(request):
    # Security check
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login_view')
        
    # 1. Fetch all stores where is_approved is False
    pending_stores = StoreProfile.objects.filter(is_approved=False).order_by('-submitted_at')
    
    # 2. Pass them to the admin dashboard
    return render(request, 'admin_home.html', {'pending_stores': pending_stores})

# NEW: The function that approves the store
def approve_store_view(request, store_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login_view')
        
    if request.method == 'POST':
        # Find the specific store and update it
        store = get_object_or_404(StoreProfile, id=store_id)
        store.is_approved = True
        store.save()
        
    # Send the admin back to the dashboard
    return redirect('admin_home_view')