import pytest
from django.contrib.auth.models import User
from insurance.models import *
from django.utils import timezone


@pytest.mark.django_db
def test_create_question(customer):
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


@pytest.mark.django_db
def test_create_policy(customer):
    # Create a Category instance
    category = Category.objects.create(category_name="Life Insurance")

    # Create a Policy instance with the created Customer and Category
    policy = Policy.objects.create(
        customer=customer,
        category=category,
        policy_name="Example Policy",
        sum_assurance=100000,
        premium=5000,
        tenure=5,
        
    )
    # Retrieve the instance from the database
    retrieved_policy = Policy.objects.get(id=policy.id)

    # Check if the values are correct
    assert retrieved_policy.customer == customer
    assert retrieved_policy.category == category
    assert retrieved_policy.policy_name == "Example Policy"
    assert retrieved_policy.sum_assurance == 100000
    assert retrieved_policy.premium == 5000
    assert retrieved_policy.tenure == 5
