


# all/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import signup, login_view ,event_list,custom_logout,add_event, home,SETTINGS,book_ticket, booking_success# Import your views
from .views import change_password_view  # Import your view
urlpatterns = [

    path('change-password/', change_password_view, name='change_password'),
    path('', home, name='home'),  # Use the home view for the root URL
    path('event_list/', event_list, name='event_list'),  # URL for the event list
    path('add/', add_event, name='add_event'),  # URL to add a new event
    path('SETTINGS/',SETTINGS, name='SETTINGS'),  
    path('book_ticket/<int:event_id>/', book_ticket, name='book_ticket'),
    path('booking_success/', booking_success, name='booking_success'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('login/', custom_logout, name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)# festive/urls.py
# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path
# from .views import event_list, add_event

# urlpatterns = [
#     path('', event_list, name='event_list'),
#     path('add/', add_event, name='add_event'),  # Add this line
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urls.py
# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path
# from django.views.generic import RedirectView  # Import RedirectView
# from .views import event_list, add_event,home # Import the home view


# urlpatterns = [
#     path('', RedirectView.as_view(url='/event_list/', permanent=False), name='home'), 
#     path('', home, name='home'),  # Redirect root to event list
#     path('event_list/', event_list, name='event_list'),  # Ensure this matches your view
#     path('add/', add_event, name='add_event'),  # URL to add a new event
# ]

# # Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path
# from .views import event_list, add_event

# urlpatterns = [
#     path('', event_list, name='event_list'),  # This will be the homepage showing the event list
#     path('add/', add_event, name='add_event'),  # This will be the URL to add a new event
# ]

# # Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns = [
#      # Use the home view for the root URL
#     path('event_list/', event_list, name='event_list'),  # Ensure this matches your view
#     path('add/', add_event, name='add_event'),  # URL to add a new event
# ]

# Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)