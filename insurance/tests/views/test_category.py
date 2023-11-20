import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.test import TestCase, Client
from insurance.models import Category


@pytest.fixture
def sample_category_data():
    return {
        "category_name": "Sample Category",
    }


@pytest.fixture
def sample_category():
    return mixer.blend("insurance.Category", category_name="Sample Category")


class AdminAddCategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_admin_add_category_view_with_valid_data(self):
        # Create a valid form data
        form_data = {"category_name": "New Category"}

        # Submit a POST request to the view
        response = self.client.post(reverse("admin-add-category"), data=form_data)

        # Assertions based on the expected behavior of your function
        self.assertEqual(
            response.status_code, 302
        )  # Check for a successful redirect status
        self.assertRedirects(response, reverse("admin-view-category"))

    def test_admin_add_category_view_invalid_form_submission(self):
        # Submit a POST request without any form data to trigger form validation errors
        response = self.client.post(reverse("admin-add-category"))

        # Assertions based on the expected behavior of your function
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        # Check for form validation errors

        # Check if the category is not added to the database
        self.assertFalse(Category.objects.exists())


@pytest.mark.django_db
def test_admin_update_category_view(client, sample_category):
    response = client.get(reverse("admin-update-category"))
    assert response.status_code == 200
    assert sample_category.category_name.encode() in response.content


class DeleteCategoryViewTest(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

    def test_delete_category_view_with_valid_category(self):
        # Create a test category
        category = Category.objects.create(category_name="Test Category")

        # Submit a POST request to delete the category
        response = self.client.post(reverse("delete-category", args=[category.pk]))

        # Assertions based on the expected behavior of your function
        self.assertEqual(
            response.status_code, 302
        )  # Check for a successful redirect status
        self.assertRedirects(response, reverse("admin-delete-category"))

        # Check if the category is deleted from the database
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())


@pytest.mark.django_db
def test_admin_view_category_view(client):
    response = client.get(reverse("admin-view-category"))

    assert response.status_code == 200
    assert "insurance/admin_view_category.html" in [t.name for t in response.templates]
    assert "categories" in response.context

    # If you want to check the number of categories or other details
    assert len(response.context["categories"]) == Category.objects.count()


@pytest.mark.django_db
def test_admin_category_view(client: Client):
    response = client.get(reverse("admin-category"))

    assert response.status_code == 200
    assert "insurance/admin_category.html" in [t.name for t in response.templates]
