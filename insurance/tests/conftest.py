import pytest
from django.contrib.auth.models import User
from insurance.models import Customer



@pytest.fixture
def customer():
    '''create a customer fixture'''
    user = User.objects.create(
        username="john doe",
        first_name="John",
        last_name="Doe",
        email="johndoe@gmail.com",
        password="password",
    )
    customer = Customer.objects.create(
        user=user,
        profile_pic=None,
        address="123 Main St",
        mobile="1234567890",
    )
    customer.save()
    return customer
