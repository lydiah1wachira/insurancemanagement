import pytest
from django.contrib.auth.models import User
from insurance.models import Question, Customer
from django.utils import timezone


@pytest.mark.django_db
def test_create_question():
    # Create a Question instance with the created Customer
    question = Question.objects.create(
        customer=customer,
        description="What is the meaning of life?",
        admin_comment="Still figuring it out...",
        asked_date=timezone.now(),
    )

    # Retrieve the instance from the database
    retrieved_question = Question.objects.get(id=question.id)

    # Check if the values are correct
    assert retrieved_question.customer == customer
    assert retrieved_question.description == "What is the meaning of life?"
    assert retrieved_question.admin_comment == "Still figuring it out..."
