from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from customer import models as CMODEL

from .. import forms, models


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "insurance/index.html")


def is_customer(user):
    return user.groups.filter(name="CUSTOMER").exists()


def afterlogin_view(request):
    """After login view."""
    if is_customer(request.user):
        return redirect("customer/customer-dashboard")
    else:
        return redirect("admin-dashboard")






