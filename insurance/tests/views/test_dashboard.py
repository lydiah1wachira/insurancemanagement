import pytest
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponseRedirect
from insurance.views.dashboard import is_customer, home_view, afterlogin_view
from django.template.response import TemplateResponse


@pytest.mark.django_db
def test_home_view_authenticated_user():
    # Create an authenticated user
    user = User.objects.create_user(username="testuser", password="testpassword")

    # Create a request with an authenticated user
    request = RequestFactory().get(reverse(""))
    request.user = user

    # Call the home_view function
    response = home_view(request)

    # Check if the response is a redirect to 'afterlogin'
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == "/afterlogin"


@pytest.mark.django_db
def test_home_view_anonymous_user():
    # Create a request with an anonymous user
    request = RequestFactory().get(reverse(""))
    request.user = AnonymousUser()

    # Call the home_view function
    response = home_view(request)

    # Check if the response is rendering 'insurance/index.html'
    assert response.status_code == 200
    assert '<p class="text-center">- Dinara</p>' in response.content.decode("utf-8")


@pytest.mark.django_db
def test_is_customer_returns_true_for_customer_user(customer_user):
    assert is_customer(customer_user) is True


@pytest.mark.django_db
def test_is_customer_returns_false_for_non_customer_user(non_customer_user):
    assert is_customer(non_customer_user) is False


@pytest.mark.django_db
def test_afterlogin_view_customer():
    # Create a customer user
    customer_user = User.objects.create_user(
        username="customer", password="testpassword"
    )
    customer_user.groups.create(name="Customers")

    # Create a request with the customer user
    request = RequestFactory().get(reverse("afterlogin"))
    request.user = customer_user

    # Call the afterlogin_view function
    response = afterlogin_view(request)

    # Check if the response is a redirect to 'customer/customer-dashboard'
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == reverse("admin-dashboard")
    
@pytest.mark.django_db
def test_afterlogin_view_non_customer():
    # Create a non-customer user
    non_customer_user = User.objects.create_user(username='admin', password='testpassword')
    
    # Create a request with the non-customer user
    request = RequestFactory().get(reverse('afterlogin'))
    request.user = non_customer_user
    
    # Call the afterlogin_view function
    response = afterlogin_view(request)
    
    # Check if the response is a redirect to 'admin-dashboard'
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == reverse('admin-dashboard')