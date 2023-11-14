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


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return HttpResponseRedirect("adminlogin")


@login_required(login_url="adminlogin")
def admin_dashboard_view(request):
    """General dashboard view."""
    dict = {
        "total_user": CMODEL.Customer.objects.all().count(),
        "total_policy": models.Policy.objects.all().count(),
        "total_category": models.Category.objects.all().count(),
        "total_question": models.Question.objects.all().count(),
        "total_policy_holder": models.PolicyRecord.objects.all().count(),
        "approved_policy_holder": models.PolicyRecord.objects.all()
        .filter(status="Approved")
        .count(),
        "disapproved_policy_holder": models.PolicyRecord.objects.all()
        .filter(status="Disapproved")
        .count(),
        "waiting_policy_holder": models.PolicyRecord.objects.all()
        .filter(status="Pending")
        .count(),
    }
    return render(request, "insurance/admin_dashboard.html", context=dict)
