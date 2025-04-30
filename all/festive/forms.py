# festive/forms.py
from django import forms
from django.contrib.auth.models import User
from django.db import models
from .models import Event  # Make sure this line is present
from .models import UserProfile  # Make sure this line is present
from .models import TicketBooking  # Make sure this line is present

class Eventmodelform(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    artist = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/')

    def __str__(self):
        return self.title
class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']  # Include any other fields you want to add

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Check if passwords match
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user

# class SignupForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("Email is already in use.")
#         return email

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError("Username is already taken.")
#         return username

# from django.contrib.auth import authenticate


# class CustomLoginForm(AuthenticationForm):
#     username_or_email = forms.CharField(label='Username or Email', max_length=254)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)

#     class Meta:
#         fields = ('username_or_email', 'password')

#     def clean(self):
#         cleaned_data = super().clean()
#         username_or_email = cleaned_data.get('username_or_email')
#         password = cleaned_data.get('password')

#         # Check if the input is an email or username
#         if username_or_email:
#             try:
#                 # Attempt to find the user by email
#                 user = User.objects.get(email=username_or_email)
#                 username = user.username
#             except User.DoesNotExist:
#                 # If not found by email, assume it's a username
#                 username = username_or_email

#             # Authenticate the user
#             user = authenticate(username=username, password=password)
#             if user is None:
#                 raise forms.ValidationError("Invalid username/email or password.")
#             else:
#                 # If authentication is successful, set the user in cleaned_data
#                 cleaned_data['user'] = user
        
#         return cleaned_data

# class CustomLoginForm(AuthenticationForm):
#     username_or_email = forms.CharField(label='Username or Email', max_length=254)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)

#     class Meta:
#         fields = ('username_or_email', 'password')

#     def clean(self):
#         cleaned_data = super().clean()
#         username_or_email = cleaned_data.get('username_or_email')
#         password = cleaned_data.get('password')

#         # Check if the input is an email or username
#         if username_or_email:
#             try:
#                 user = User.objects.get(email=username_or_email)
#                 username = user.username
#             except User.DoesNotExist:
#                 username = username_or_email

#             # Authenticate the user
#             user = authenticate(username=username, password=password)
#             if user is None:
#                 raise forms.ValidationError("Invalid username/email or password.")
        
#         return cleaned_data
# class SignupForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#         return user


# class CustomLoginForm(AuthenticationForm):
#     username_or_email = forms.CharField(label='Username or Email', max_length=254)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)

#     class Meta:
#         fields = ('username_or_email', 'password')
# class SignupForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
# class CustomLoginForm(AuthenticationForm):
#     username_or_email = forms.CharField(label='Username or Email', max_length=254)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)

#     class Meta:
#         fields = ('username_or_email', 'password')

# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ['title', 'description', 'date','artist', 'location','image']
# forms.py

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'artist', 'location', 'image', 'ticket_price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'ticket_price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo', 'bio']
# forms.py


class TicketBookingForm(forms.ModelForm):
    class Meta:
        model = TicketBooking
        fields = ['event', 'number_of_tickets']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'number_of_tickets': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }