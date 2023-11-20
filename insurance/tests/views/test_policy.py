import pytest
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from insurance import models
from django.urls import reverse
from django.contrib.auth.models import User
from insurance.views.policy_views import admin_policy_view
from django.shortcuts import render
from django.test import RequestFactory
from customer.models import Customer


@pytest.fixture
def admin_user(db):
    return mixer.blend(User, is_staff=True, is_superuser=True)


@pytest.fixture
def sample_category_data():
    return {
        "category_name": "Test Category",
        "creation_date": "2023-01-01",  # Replace with an appropriate date
    }


@pytest.fixture
def sample_policy_data():
    return {
        "category": mixer.blend(models.Category).id,
        "policy_name": "Test Policy",
        "sum_assurance": 10000,
        "premium": 500,
        "tenure": 12,
        "creation_date": "2023-01-01",  # Replace with an appropriate date
    }


@pytest.mark.django_db
def test_admin_add_policy_view(
    client, admin_user, sample_category_data, sample_policy_data
):
    # Create a category to be used in the form
    response_category = client.post(
        reverse("admin-add-category"), data=sample_category_data
    )
    assert response_category.status_code == 302

    # Log in the admin user
    client.force_login(admin_user)

    # Get the created category for the policy form
    category_id = models.Category.objects.last().id

    # Create a request with POST data
    request_data = {
        "category": category_id,
        "policy_name": "Test Policy",
        "sum_assurance": 10000,
        "premium": 500,
        "tenure": 12,
        "creation_date": "2023-01-01",  # Replace with an appropriate date
    }

    response = client.post(reverse("admin-add-policy"), data=request_data)

    # Assert that the response is a redirect to 'admin-view-policy'
    assert response.status_code == 302
    assert response.url == reverse("admin-view-policy")

    # Assert that the policy was created
    assert models.Policy.objects.filter(policy_name="Test Policy").exists()


class UpdatePolicyViewTest(TestCase):
    def setUp(self):
        # Create a user for testing (you may adjust this as needed)
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a category for the policy
        self.category = models.Category.objects.create(category_name="TestCategory")

        # Create a policy for testing
        self.policy = models.Policy.objects.create(
            policy_name="TestPolicy",
            sum_assurance=500,
            premium=500,
            tenure=10,
            category=self.category,
        )

    def test_update_policy_view(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Prepare the updated data
        updated_data = {
            "policy_name": "UpdatedPolicy",
            "sum_assurance": 600,
            "category": self.category.id,
            "premium": 700,
            "tenure": 80,
            # Add other fields as needed
        }

        # Get the update URL for the specific policy
        update_url = reverse("update-policy", args=[self.policy.id])

        # Simulate a POST request to update the policy
        response = self.client.post(update_url, data=updated_data)

        # Check if the update was successful (you may adjust this based on your redirect logic)
        self.assertRedirects(response, reverse("admin-update-policy"))

        # Retrieve the policy again to check if it was updated in the database
        updated_policy = models.Policy.objects.get(id=self.policy.id)

        self.assertEqual(updated_policy.policy_name, "UpdatedPolicy")
        self.assertEqual(updated_policy.tenure, 80)
        self.assertEqual(updated_policy.category, self.category)


def test_admin_policy_view():
    # Create a request object
    request = RequestFactory().get("/admin_policy/")

    # Call the view function
    response = admin_policy_view(request)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the correct template is used in the response
    assert (
        '<h6 class="m-b-20"><a href="admin-view-disapproved-policy-holder" style="text-decoration: none;color:white;">Disapproved Policy Holder</a></h6>\n'
        in response.content.decode("utf-8")
    )


class AdminViewPolicyViewTests(TestCase):
    def setUp(self):
        # Set up a test user with admin privileges
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpassword"
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        # Log in the admin user
        self.client = Client()
        self.client.login(username="admin", password="adminpassword")

        # Set up test data
        self.category = models.Category.objects.create(category_name="Test Category")
        self.policy = models.Policy.objects.create(
            category=self.category,
            policy_name="Test Policy",
            sum_assurance=100000,
            premium=5000,
            tenure=12,
        )

    def test_admin_view_policy_view(self):
        response = self.client.get(reverse("admin-view-policy"))

        # Check if the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check if the rendered template contains the policy name
        self.assertContains(response, "Test Policy")

        # Check if the policies are passed to the context
        policies = response.context["policies"]
        self.assertEqual(list(policies), [self.policy])


class AdminDeletePolicyViewTests(TestCase):
    def setUp(self):
        # Set up a test user with admin privileges
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpassword"
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        # Log in the admin user
        self.client = Client()
        self.client.login(username="admin", password="adminpassword")

        # Set up test data
        self.category = models.Category.objects.create(category_name="Test Category")
        self.policy = models.Policy.objects.create(
            category=self.category,
            policy_name="Test Policy",
            sum_assurance=100000,
            premium=5000,
            tenure=12,
        )

        self.customer_user = User.objects.create_user(
            username="customer", password="customerpassword"
        )
        self.customer = Customer.objects.create(
            user=self.customer_user,
            address="Test Address",
            mobile="1234567890",
        )

        self.policy_record = models.PolicyRecord.objects.create(
            customer=self.customer,
            Policy=self.policy,
            status="Pending",
        )

        self.approved_policy_record_instance = models.PolicyRecord.objects.create(
            customer=self.customer,
            Policy=self.policy,
            status="Approved",
        )

        self.pending_policy_record_instance = models.PolicyRecord.objects.create(
            customer=self.customer,
            Policy=self.policy,
            status="Pending",
        )

        self.disapproved_policy_record_instance = models.PolicyRecord.objects.create(
            customer=self.customer,
            Policy=self.policy,
            status="Disapproved",
        )

    def test_admin_delete_policy_view(self):
        response = self.client.get(reverse("admin-delete-policy"))

        # Check if the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check if the rendered template contains the policy name
        self.assertContains(response, "Test Policy")

        # Check if the policies are passed to the context
        policies = response.context["policies"]
        self.assertEqual(list(policies), [self.policy])

    def test_delete_policy_view(self):
        # Get the policy ID for the policy created in the setup
        policy_id = self.policy.id

        # Send a POST request to delete the policy
        response = self.client.post(reverse("delete-policy", args=[policy_id]))

        # Check if the view redirects to the expected URL
        self.assertRedirects(response, reverse("admin-delete-policy"))

        # Check if the policy is deleted from the database
        self.assertFalse(models.Policy.objects.filter(id=policy_id).exists())

    def test_admin_view_policy_holder_view(self):
        response = self.client.get(reverse("admin-view-policy-holder"))

        # Check if the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check if the rendered template contains the policy holder's name
        self.assertContains(response, self.customer.get_name)

        # Check if the policy records are passed to the context
        policyrecords = response.context["policyrecords"]
        self.assertEqual(list(policyrecords), [self.policy_record])

    def test_admin_view_approved_policy_holder_view(self):
        response = self.client.get(reverse("admin-view-approved-policy-holder"))

        # Check if the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check if the rendered template contains the policy holder's name
        self.assertContains(response, self.customer.get_name)

        # Check if only approved policy records are present in the context
        policyrecords = response.context["policyrecords"]
        self.assertEqual(list(policyrecords), [self.approved_policy_record_instance])

    def test_admin_view_disapproved_policy_holder_view(self):
        response = self.client.get(reverse("admin-view-disapproved-policy-holder"))

        # Check if the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check if the rendered template contains the policy holder's name
        self.assertContains(response, self.customer.get_name)

        # Check if only disapproved policy records are present in the context
        policyrecords = response.context["policyrecords"]
        self.assertEqual(list(policyrecords), [self.disapproved_policy_record_instance])

    def test_admin_view_waiting_policy_holder_view(self):
        response = self.client.get(reverse("admin-view-waiting-policy-holder"))

        # Check if the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check if the rendered template contains the policy holder's name
        self.assertContains(response, self.customer.get_name)

        # Check if only pending policy records are present in the context
        policyrecords = response.context["policyrecords"]
        self.assertEqual(list(policyrecords), [self.pending_policy_record_instance])
