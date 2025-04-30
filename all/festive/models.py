from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from datetime import time
class Event(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100, default='Unknown Artist')
    description = models.TextField()
    date = models.DateTimeField()
    time = models.TimeField(default=time(12, 0)) 
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add ticket price
     # Store event time
    @classmethod
    def get_default_time(cls):
        # You can change this logic to return a different default time
        return time(12, 0)  # Default time can be changed here

    def save(self, *args, **kwargs):
        if not self.time:  # If time is not set, use the default
            self.time = self.get_default_time()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add balance field

    def __str__(self):
        return self.user.username

# Automatically create a UserProfile when a User is created
@receiver(post_save, sender=User )
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Automatically save the UserProfile when the User is saved
@receiver(post_save, sender=User )
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()   
class TicketBooking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_tickets = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Set a default value
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number_of_tickets} tickets for {self.event.title}"
