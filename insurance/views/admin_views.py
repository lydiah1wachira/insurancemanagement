from datetime import date, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic import CreateView, ListView, TemplateView
from customer import forms as CFORM
from customer import models as CMODEL
from .. import forms, models
from ..models import Category, Customer, Question


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


@login_required(login_url="adminlogin")
def admin_view_customer_view(request):
    """view function to display all customers to the admin"""

    customers = CMODEL.Customer.objects.all()

    return render(
        request, "insurance/admin_view_customer.html", {"customers": customers}
    )


@login_required(login_url="adminlogin")
def update_customer_view(request, pk):
    """view functioner for thr form to update customers and their details"""

    customer = CMODEL.Customer.objects.get(id=pk)
    user = CMODEL.User.objects.get(id=customer.user_id)
    userForm = CFORM.CustomerUserForm(instance=user)
    customerForm = CFORM.CustomerForm(request.FILES, instance=customer)
    mydict = {"userForm": userForm, "customerForm": customerForm}

    if request.method == "POST":
        userForm = CFORM.CustomerUserForm(request.POST, instance=user)
        customerForm = CFORM.CustomerForm(
            request.POST, request.FILES, instance=customer
        )
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect("admin-view-customer")

    return render(request, "insurance/update_customer.html", context=mydict)


@login_required(login_url="adminlogin")
def delete_customer_view(request, pk):
    """view function to handle a customer deletion"""

    customer = CMODEL.Customer.objects.get(id=pk)
    user = User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()

    return HttpResponseRedirect("/admin-view-customer")
