import pytest
from django.urls import reverse
from django.core import mail


# Tests for the About us view
@pytest.mark.django_db
def test_aboutus_view_returns_200(client):
    response = client.get(reverse("aboutus_view"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_aboutus_view_uses_correct_template(client):
    response = client.get(reverse("aboutus_view"))
    assert "insurance/aboutus.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_aboutus_view_content(client):
    response = client.get(reverse("aboutus_view"))
    assert "<p>Explore our Website.</p>" in str(response.content)


# Tests for the contact us view
@pytest.mark.django_db
def test_contactus_view_get(client):
    response = client.get(reverse("contactus_view"))
    assert response.status_code == 200
    assert "insurance/contactus.html" in [t.name for t in response.templates]
    assert "form" in response.context


@pytest.mark.django_db
def test_contactus_view_post_valid_form(client):
    data = {
        "Name": "John Doe",
        "Email": "john@example.com",
        "Message": "This is a test message.",
    }
    response = client.post(reverse("contactus_view"), data)

    assert response.status_code == 200
    assert "insurance/contactussuccess.html" in [t.name for t in response.templates]
    assert len(mail.outbox) == 1  # Check that an email was sent
    assert (
        mail.outbox[0].subject == "John Doe || john@example.com"
    )  # Check the email subject


@pytest.mark.django_db
def test_contactus_view_post_invalid_form(client):
    data = {
        "Name": "",  # Invalid, as the name is required
        "Email": "john@example.com",
        "Message": "This is a test message.",
    }
    response = client.post(reverse("contactus_view"), data)

    assert response.status_code == 200
    assert "insurance/contactus.html" in [t.name for t in response.templates]
    assert "form" in response.context
    assert response.context["form"].errors  # Check that form validation errors exist
