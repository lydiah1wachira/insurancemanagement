from django.contrib import admin
from django.urls import path
from insurance.views import *
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("customer/", include("customer.urls")),
    path("", include("insurance.urls")),
]
