from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from customer import forms as CFORM
from customer import models as CMODEL


@login_required(login_url="adminlogin")
def admin_view_customer_view(request):
    """View to display all customers"""
    customers = CMODEL.Customer.objects.all()
    return render(
        request, "insurance/admin_view_customer.html", {"customers": customers}
    )


@login_required(login_url="adminlogin")
def update_customer_view(request, pk):
    """Update a specific customer view."""
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
    """Delete a specific customer view."""
    customer = CMODEL.Customer.objects.get(id=pk)
    user = User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect("/admin-view-customer")
