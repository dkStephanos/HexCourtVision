"""
Definition of urls for NBA_Thesis.
"""

from datetime import datetime
from django.conf.urls import url
from django.urls import path
import django.contrib.auth.views
from django.conf.urls import include
from django.contrib import admin


import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
]
