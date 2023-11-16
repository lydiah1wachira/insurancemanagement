import pytest
from customer import models as CMODEL
from django.contrib.auth.models import User
from django.urls import reverse
from mixer.backend.django import mixer

from insurance.models import Category, Policy

from .. import models


@pytest.fixture
def create_category():
    def _create_category(category_name="Test Category"):
        return Category.objects.create(category_name=category_name)

    return _create_category

@pytest.fixture
def create_policy(create_category):
    def _create_policy(
        category=None,
        policy_name="Test Policy",
        sum_assurance=1000,
        premium=100,
        tenure=1,
    ):
        if category is None:
            category = create_category()
        return Policy.objects.create(
            category=category,
            policy_name=policy_name,
            sum_assurance=sum_assurance,
            premium=premium,
            tenure=tenure,
        )

    return _create_policy

@pytest.fixture
def admin_user():
    return User.objects.create_user(username='admin', password='adminpassword', is_staff=True)

@pytest.fixture
def client(admin_user):
    from django.test import Client
    client = Client()
    client.login(username='admin', password='adminpassword')
    return client

@pytest.fixture
def sample_category():
    return mixer.blend('insurance.Category')

@pytest.fixture
def sample_category_data():
    return {'name': 'Sample Category'}


@pytest.fixture
def admin_user():
    return User.objects.create_user(username='admin', password='adminpassword', is_staff=True)

@pytest.fixture
def client(admin_user):
    from django.test import Client
    client = Client()
    client.login(username='admin', password='adminpassword')
    return client

@pytest.fixture
def sample_customer_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
        'first_name': 'Test',
        'last_name': 'User',
        'address': 'Test Address',
        'mobile': '1234567890',
        'profile_pic': 'path/to/profile_pic.jpg'
    }

@pytest.fixture
def sample_customer(sample_customer_data):
    user = mixer.blend(User, **sample_customer_data)
    customer = mixer.blend(CMODEL.Customer, user=user)
    return customer



@pytest.fixture
def update_customer_data():
    return {
        'username': 'updateduser',
        'password': 'updatedpassword',
        'first_name': 'Updated',
        'last_name': 'User',
        'address': 'Updated Address',
        'mobile': '9876543210',
        # 'profile_pic': 'path/to/updated_profile_pic.jpg'
    }

@pytest.fixture
def update_customer_view_client(client, sample_customer):
    return client.get(reverse('update_customer_view', args=[sample_customer.pk]))

@pytest.fixture
def delete_customer_view_client(client, sample_customer):
    return client.get(reverse('delete_customer_view', args=[sample_customer.pk]))


@pytest.fixture
def admin_user():
    return User.objects.create_user(username='admin', password='adminpassword', is_staff=True)

@pytest.fixture
def client(admin_user):
    from django.test import Client
    client = Client()
    client.login(username='admin', password='adminpassword')
    return client

@pytest.fixture
def sample_category():
    return mixer.blend('insurance.Category')

@pytest.fixture
def sample_policy_data(sample_category):
    return {
        'policy_name': 'Test Policy',
        'sum_assurance': 10000,
        'premium': 500,
        'tenure': 12,
        'category': sample_category,
    }

@pytest.fixture
def sample_policy(client, sample_policy_data):
    return mixer.blend(models.Policy, **sample_policy_data)

@pytest.fixture
def sample_policy_record(sample_policy):
    return mixer.blend(models.PolicyRecord, policy=sample_policy)

@pytest.fixture
def update_policy_data(sample_category):
    return {
        'policy_name': 'Updated Policy',
        'sum_assurance': 15000,
        'premium': 700,
        'tenure': 24,
        'category': sample_category,
    }

@pytest.fixture
def update_policy_view_client(client, sample_policy):
    return client.get(reverse('update_policy_view', args=[sample_policy.pk]))

@pytest.fixture
def delete_policy_view_client(client, sample_policy):
    return client.get(reverse('delete_policy_view'))

@pytest.fixture
def sample_policy_record_data():
    return {
        'customer': mixer.blend(models.Customer),
        'policy': mixer.blend(models.Policy),
        'status': 'Pending',
    }

@pytest.fixture
def sample_approved_policy_record(sample_policy):
    return mixer.blend(models.PolicyRecord, policy=sample_policy, status='Approved')

@pytest.fixture
def sample_disapproved_policy_record(sample_policy):
    return mixer.blend(models.PolicyRecord, policy=sample_policy, status='Disapproved')

@pytest.fixture
def sample_waiting_policy_record(sample_policy):
    return mixer.blend(models.PolicyRecord, policy=sample_policy, status='Pending')



