import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, Group
from customer.models import Customer
from insurance.views import admin_views


@pytest.mark.django_db
def test_authenticated_user_redirect_to_afterlogin(client):
    client.login(username="user", password="password")
    response = client.get(reverse("adminclick_view"))
    assert response.status_code == 302
    assert response.url == reverse("afterlogin")
