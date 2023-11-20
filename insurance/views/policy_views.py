from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .. import forms, models


def admin_policy_view(request):
    '''view to display the policy page'''
    return render(request, "insurance/admin_policy.html")


def admin_add_policy_view(request):
    '''view to display form for admin to add a new policy'''
    policyForm = forms.PolicyForm()

    if request.method == "POST":
        policyForm = forms.PolicyForm(request.POST)
        if policyForm.is_valid():
            categoryid = request.POST.get("category")
            category = models.Category.objects.get(id=categoryid)

            policy = policyForm.save(commit=False)
            policy.category = category
            policy.save()
            return redirect("admin-view-policy")
    return render(
        request, "insurance/admin_add_policy.html", {"policyForm": policyForm}
    )


def admin_view_policy_view(request):
    '''view to display all policies to the admin'''
    policies = models.Policy.objects.all()
    return render(request, "insurance/admin_view_policy.html", {"policies": policies})


def admin_update_policy_view(request):
    '''update policies view'''
    policies = models.Policy.objects.all()
    return render(request, "insurance/admin_update_policy.html", {"policies": policies})


@login_required(login_url="adminlogin")
def update_policy_view(request, pk):
    '''view to update a specific policy'''
    policy = models.Policy.objects.get(id=pk)
    policyForm = forms.PolicyForm(instance=policy)

    if request.method == "POST":
        policyForm = forms.PolicyForm(request.POST, instance=policy)

        if policyForm.is_valid():
            categoryid = request.POST.get("category")
            category = models.Category.objects.get(id=categoryid)

            policy = policyForm.save(commit=False)
            policy.category = category
            policy.save()

            return redirect("admin-update-policy")
    return render(request, "insurance/update_policy.html", {"policyForm": policyForm})


def admin_delete_policy_view(request):
    '''Delete policies views'''
    policies = models.Policy.objects.all()
    return render(request, "insurance/admin_delete_policy.html", {"policies": policies})


def delete_policy_view(request, pk):
    '''Delete specific policy view'''
    policy = models.Policy.objects.get(id=pk)
    policy.delete()
    return redirect("admin-delete-policy")


def admin_view_policy_holder_view(request):
    '''view to display all policy records to admin'''
    policyrecords = models.PolicyRecord.objects.all()
    return render(
        request,
        "insurance/admin_view_policy_holder.html",
        {"policyrecords": policyrecords},
    )


def admin_view_approved_policy_holder_view(request):
    '''display all approved records to admin view'''
    policyrecords = models.PolicyRecord.objects.all().filter(status="Approved")
    return render(
        request,
        "insurance/admin_view_approved_policy_holder.html",
        {"policyrecords": policyrecords},
    )


def admin_view_disapproved_policy_holder_view(request):
    '''view to display all disapproved policies'''
    policyrecords = models.PolicyRecord.objects.all().filter(status="Disapproved")
    return render(
        request,
        "insurance/admin_view_disapproved_policy_holder.html",
        {"policyrecords": policyrecords},
    )


def admin_view_waiting_policy_holder_view(request):
    '''view to display all policies pending approval'''
    policyrecords = models.PolicyRecord.objects.all().filter(status="Pending")
    return render(
        request,
        "insurance/admin_view_waiting_policy_holder.html",
        {"policyrecords": policyrecords},
    )


def approve_request_view(request, pk):
    '''Views to handle a specific approved policy'''
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status = "Approved"
    policyrecords.save()
    return redirect("admin-view-policy-holder")


def disapprove_request_view(request, pk):
    '''view to display a sepecific disapproved policy'''
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status = "Disapproved"
    policyrecords.save()
    return redirect("admin-view-policy-holder")

