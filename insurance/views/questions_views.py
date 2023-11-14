from django.shortcuts import redirect, render
from .. import forms, models


def admin_question_view(request):
    '''view to display all questions to the admin by customers'''
    questions = models.Question.objects.all()
    return render(request, "insurance/admin_question.html", {"questions": questions})


def update_question_view(request, pk):
    """Update a specific question view."""
    question = models.Question.objects.get(id=pk)
    questionForm = forms.QuestionForm(instance=question)

    if request.method == "POST":
        questionForm = forms.QuestionForm(request.POST, instance=question)

        if questionForm.is_valid():
            admin_comment = request.POST.get("admin_comment")

            question = questionForm.save(commit=False)
            question.admin_comment = admin_comment
            question.save()

            return redirect("admin-question")
    return render(
        request, "insurance/update_question.html", {"questionForm": questionForm}
    )
