import pytest
from django.urls import reverse
from insurance.models import Question
from datetime import date


@pytest.mark.django_db
def test_admin_question_view(client, admin_user, question):
    client.login(username="admin", password="password")  # Log in as the admin user

    response = client.get(reverse("admin-question"))

    assert response.status_code == 200
    assert "insurance/admin_question.html" in [t.name for t in response.templates]
    assert "questions" in response.context

    # Check if the question is present in the rendered HTML
    assert f"<th> Problem</th>" in str(response.content)


@pytest.mark.django_db
def test_update_question_view_get(client, question):
    client.login(username="admin", password="password")  # Log in as the admin user

    response = client.get(reverse("update-question", kwargs={"pk": question.id}))

    assert response.status_code == 200
    assert "insurance/update_question.html" in [t.name for t in response.templates]
    assert "questionForm" in response.context


@pytest.mark.django_db
def test_update_question_view_post_valid_form(client, admin_user, question):
    client.login(username="admin", password="password")  # Log in as the admin user

    data = {
        "customer": question.customer.id,
        "description": "Updated Question Description",
        "admin_comment": "Updated Admin Comment",
    }

    response = client.post(
        reverse("update-question", kwargs={"pk": question.id}), data
    )

    assert response.status_code == 302  # Redirect status code
    assert response.url == reverse(
        "admin-question"
    )  # Check if redirected to the correct URL

    updated_question = Question.objects.get(id=question.id)
    assert updated_question.description == "Updated Question Description"
    assert updated_question.admin_comment == "Updated Admin Comment"
