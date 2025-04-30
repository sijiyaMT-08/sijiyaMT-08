# from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm
from django.db.models import Q  # Import Q for complex queries
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib import messages
from .forms import CustomLoginForm,SignupForm
from django.contrib.auth.models import User
from .forms import TicketBookingForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, TicketBooking, UserProfile # Ensure this form is defined
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.backends import ModelBackend  # Import this
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Ensure the user is authenticated with a valid backend
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            messages.success(request, "Signup successful! Welcome!")
            return redirect('event_list')  # Ensure 'event_list' is correctly mapped in URLs
        else:
            messages.error(request, "There were errors in your signup form.")
    else:
        form = SignupForm()
    
    return render(request, 'festive/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)  # Correctly initialize the form
        if form.is_valid():
            print("Form is valid")
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            print(f"Attempting to log in with: {username_or_email}")

            User = get_user_model()
            try:
                # Check if the input is an email or username
                if '@' in username_or_email:
                    user = User.objects.get(email=username_or_email)
                else:
                    user = User.objects.get(username=username_or_email)

                # Attempt to authenticate the user
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful! Welcome back.")
                return redirect('event_list')
            else:
                messages.error(request, "Invalid username/email or password.")
                print("Authentication failed")
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    else:
        form = CustomLoginForm()
    
    return render(request, 'festive/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to the login page or homepage


def event_list(request):
    # Get filter parameters from the request
    location = request.GET.get('location')
    artist = request.GET.get('artist')
    date = request.GET.get('date')
    time = request.GET.get('time')

    # Start with all events
    events = Event.objects.all()

    # Apply filters if provided
    if location:
        events = events.filter(location__icontains=location)  # Filter by location
    if artist:
        events = events.filter(artist__icontains=artist)  # Filter by artist
    if date:
        events = events.filter(date__icontains=date)  # Filter by location
    if time:
        events = events.filter(time__icontains=time)

    # Order the events by date
    events = events.order_by('date')

    return render(request, 'festive/event_list.html', {'events': events})

@login_required
def book_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            number_of_tickets = form.cleaned_data['number_of_tickets']
            total_price = number_of_tickets * event.ticket_price
            
            user_profile = get_object_or_404(UserProfile, user=request.user)
            if user_profile.balance >= total_price:
                # Create the ticket booking
                TicketBooking.objects.create(
                    user=request.user,
                    event=event,
                    number_of_tickets=number_of_tickets,
                    total_price=total_price
                )
                # Deduct the total price from the user's balance
                user_profile.balance -= total_price
                user_profile.save()
                messages.success(request, 'Booking successful!')
                return redirect('booking_success')  # Redirect to a success page
            else:
                messages.error(request, 'Insufficient balance.')
                return redirect('event_list')  # Redirect back to event list
    else:
        form = TicketBookingForm()

    return render(request, 'festive/book_ticket.html', {'form': form, 'event': event})

def booking_success(request):
    return render(request, 'festive/booking_success.html')

def add_event(request):
    if request.method == 'POST':
        event_title = request.POST.get('event_title')
        event_description = request.POST.get('event_description')
        event_date = request.POST.get('event_date')
        event_time =request.post.get('event_time')
        artist = request.POST.get('artist')
        event_location = request.POST.get('event_location')
        event_image = request.FILES.get('event_image')
        ticket_price = request.POST.get('ticket_price')  # Get ticket price from form

        # Create and save the event
        event = Event(
            title=event_title,
            description=event_description,
            date=event_date,
            time=event_time,
            artist=artist,
            location=event_location,
            image=event_image,
            ticket_price=ticket_price  # Set ticket price
        )
        event.save()

        # Add a success message
        messages.success(request, 'Event added successfully!')

        # Redirect to the event list or another page
        return redirect('event_list')  # Adjust the redirect as needed

    return render(request, 'festive/add_event.html')# views.py



def SETTINGS(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Handle user profile updates
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            # Handle profile update
            if 'update_profile' in request.POST:
                profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
                if profile_form.is_valid():
                    profile_form.save()
                    messages.success(request, "Profile updated successfully.")
                    return redirect('SETTINGS')

            # Handle signup
            elif 'signup' in request.POST:
                signup_form = UserCreationForm(request.POST)
                if signup_form.is_valid():
                    user = signup_form.save()
                    UserProfile.objects.create(user=user)  # Create a user profile
                    messages.success(request, "Account created successfully! Please log in.")
                    return redirect('home')

            # Handle login
            elif 'login' in request.POST:
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in successfully.")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid username or password.")

            # Handle logout
            elif 'logout' in request.POST:
                logout(request)
                messages.success(request, "Logged out successfully.")
                return redirect('home')

        else:
            profile_form = UserProfileForm(instance=user_profile)
            signup_form = UserCreationForm()

        return render(request, 'festive/SETTINGS.html', {
            'profile_form': profile_form,
            'signup_form': signup_form,
            'user_profile': user_profile,
        })
    else:
        # If the user is not authenticated, show the login and signup forms
        if request.method == 'POST':
            # Handle signup
            if 'signup' in request.POST:
                signup_form = UserCreationForm(request.POST)
                if signup_form.is_valid():
                    user = signup_form.save()
                    UserProfile.objects.create(user=user)  # Create a user profile
                    messages.success(request, "Account created successfully! Please log in.")
                    return redirect('home')

            # Handle login
            elif 'login' in request.POST:
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in successfully.")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid username or password.")

        signup_form = UserCreationForm()
        return render(request, 'festive/SETTINGS.html', {
            'signup_form': signup_form,
        })

def home(request):
    return render(request, 'festive/home.html')  # Use the correct path # Render the home page template  # Redirect to the event list
  # Render the settings page template
# def event_list(request):
#     # Get filter parameters from the request
#     location = request.GET.get('location')
#     artist = request.GET.get('artist_name')

#     # Start with all events
#     events = Event.objects.all()

#     # Apply filters if provided
#     if location:
#         events = events.filter(location__icontains=location)  # Filter by location
#     if artist:
#         events = events.filter(artist__icontains=artist)  # Filter by artist

#     # Order the events by date
#     events = events.order_by('date')

#     return render(request, 'festive/event_list.html', {'events': events})
 # Assuming you have an Event model
def add_event(request):
    if request.method == 'POST':
        event_title = request.POST.get('event_title')
        event_description = request.POST.get('event_description')
        event_date = request.POST.get('event_date')
        artist = request.POST.get('artist')
        event_location = request.POST.get('event_location')
        event_image = request.FILES.get('event_image')

        # Create and save the event
        event = Event(
            title=event_title,
            description=event_description,
            date=event_date,
            artist=artist,
            location=event_location,
            image=event_image
        )
        event.save()

        # Add a success message
        messages.success(request, 'Event added successfully!')

        # Redirect to the event list or another page
        return redirect('event_list')  # Adjust the redirect as needed

    return render(request, 'festive/add_event.html')  # Replace with your actual template
# Assuming you have a form class for Event

# def add_event(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Event added successfully.")
#             return redirect('event_list')  # Redirect to the event list after successful submission
#     else:
#         form = EventForm()
#     return render(request, 'festive/add_event.html', {'form': form})

# def add_event(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
#         if form.is_valid():
#             form.save()
#             return redirect('event_list')  # Redirect to the event list or another page
#     else:
#         form = EventForm()
#     return render(request, 'festive/add_event.html', {'form': form})
from django.views.generic import ListView


class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.GET.get('location')
        artist = self.request.GET.get('artist')

        if location:
            queryset = queryset.filter(location__icontains=location)
        
        if artist:
            queryset = queryset.filter(artist__icontains=artist)

        return queryset
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('settings')  # Redirect to the settings page or wherever you want
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'your_template.html', {'form': form})  # Replace with your template

# def login_view(request):
#     if request.method == 'POST':
#         form = CustomLoginForm(request, data=request.POST)
#         if form.is_valid():
#             print("Form is valid")
#             username_or_email = form.cleaned_data.get('username_or_email')
#             password = form.cleaned_data.get('password')
#             print(f"Attempting to log in with: {username_or_email}")

#             User = get_user_model()
#             try:
#                 # Check if the input is an email or username
#                 if '@' in username_or_email:
#                     user = User.objects.get(email=username_or_email)
#                 else:
#                     user = User.objects.get(username=username_or_email)

#                 # Attempt to authenticate the user
#                 user = authenticate(request, username=user.username, password=password)
#             except User.DoesNotExist:
#                 user = None

#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "Login successful! Welcome back.")
#                 return redirect('event_list')
#             else:
#                 messages.error(request, "Invalid username/email or password.")
#                 print("Authentication failed")
#         else:
#             print("Form is not valid")
#             print(form.errors)  # Print form errors for debugging
#     else:
#         form = CustomLoginForm()
    
#     return render(request, 'festive/login.html', {'form': form})
# def custom_logout(request):
#     logout(request)
#     messages.success(request, "You have been logged out successfully.")
#     return render(request, 'logged_out.html')  # Render a custom template
# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Save the new user
#             login(request, user)  # Log the user in after signup
#             messages.success(request, "Signup successful! Welcome!")
#             return redirect('event_list')  # Redirect to the event list after successful signup
#         else:
#             print(form.errors)  # Print form errors for debugging
#     else:
#         form = SignupForm()
#     return render(request, 'festive/signup.html', {'form': form})