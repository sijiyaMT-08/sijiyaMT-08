# admin.py
from django.contrib import admin
from .models import Event, UserProfile, TicketBooking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'date', 'location', 'created_at')
    search_fields = ('title', 'artist', 'location')
    list_filter = ('date',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'user__email')

@admin.register(TicketBooking)
class TicketBookingAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'number_of_tickets', 'booked_at')
    search_fields = ('event__title', 'user__username')# from django.contrib import admin

# # festive/admin.py
# from .models import Event

# @admin.register(Event)

# class EventAdmin(admin.ModelAdmin):
#     list_display = ('title', 'artist', 'date', 'location', 'created_at')  # Added artist
#     search_fields = ('title', 'location', 'artist')  # Added artist to search fields
#     list_filter = ('date',)

# Register your models here.
# myapp/admin.py

# from .models import Event

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('title', 'date', 'location')  # Fields to display in the list view
#     search_fields = ('title', 'location')  # Fields to search in the admin interface
#     list_filter = ('date',)  # Add filters for the list view

# Alternatively, you can register the model without a custom admin class
# admin.site.register(Event)
