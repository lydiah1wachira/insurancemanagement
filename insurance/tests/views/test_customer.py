import pytest
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import render
from customer.models import Customer
from customer.forms import CustomerUserForm, CustomerForm
from insurance.views.customer_views import (
    admin_view_customer_view,
    update_customer_view,
)


@pytest.mark.django_db
def test_admin_view_customer_view(client):
    # Create a customer for testing
    customer = Customer.objects.create(
        user_id="1", profile_pic="pic_url", address="Test Customer", mobile="98766906"
    )

    # Set up request and call the view function
    url = reverse("admin-view-customer")
    response = client.get(url)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the customer's data is present in the response
    assert customer.address in str(response.content)
    assert customer.mobile in str(response.content)

    # Check if the template used is correct
    assert "insurance/admin_view_customer.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_update_customer_view_get(client):
    user = User.objects.create(username="testuser", password="testpassword")
    customer = Customer.objects.create(
        user=user, profile_pic="progile_pic", address="address", mobile="23456"
    )

    url = reverse("update-customer", kwargs={"pk": customer.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert "userForm" in response.context
    assert "customerForm" in response.context
    assert "insurance/update_customer.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
def test_update_customer_view_post_valid_data(client):
    user = User.objects.create(username="testuser", password="testpassword")
    customer = Customer.objects.create(
        user=user, profile_pic="profile_pic", address="address", mobile="23456"
    )

    url = reverse("update-customer", kwargs={"pk": customer.pk})
    data = {
        "username": "newusername",
        # Include other required form fields in the data
    }
    response = client.post(url, data)

    # Check for a successful redirect (status code 302)
    assert response.status_code == 200

    # Get the redirected URL from the 'Location' header
    redirect_url = response.headers["Location"]

    # Check that the redirect URL matches the expected URL
    expected_redirect_url = reverse("admin-view-customer")
    assert redirect_url == expected_redirect_url

    # Check that the customer was updated with the new data
    updated_customer = Customer.objects.get(pk=customer.pk)
    assert updated_customer.user.username == "newusername"


@pytest.mark.django_db
def test_update_customer_view_post_invalid_data(client):
    user = User.objects.create(username="testuser", password="testpassword")
    customer = Customer.objects.create(
        user=user, profile_pic="progile_pic", address="address", mobile="23456"
    )

    url = reverse("update-customer", kwargs={"pk": customer.pk})
    data = {
        # Include incomplete or invalid data to test form validation
    }
    response = client.post(url, data)

    assert response.status_code == 200
    # Check that the form errors are present in the response
    assert "userForm" in response.context
    assert "customerForm" in response.context
    assert response.context["userForm"].errors
    assert response.context["customerForm"].errors
