from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .. import forms


def aboutus_view(request):
    """An about us view"""
    return render(request, "insurance/aboutus.html")


def contactus_view(request):
    """A contact Us view."""
    sub = forms.ContactusForm()
    if request.method == "POST":
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data["Email"]
            name = sub.cleaned_data["Name"]
            message = sub.cleaned_data["Message"]
            send_mail(
                str(name) + " || " + str(email),
                message,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_RECEIVING_USER,
                fail_silently=False,
            )
            return render(request, "insurance/contactussuccess.html")
    return render(request, "insurance/contactus.html", {"form": sub})
