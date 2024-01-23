"""
Definition of urls for NBA_Thesis.
"""

from django.urls import path
from django.conf.urls import include
from django.contrib import admin

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
]
