from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .. import forms, models
from ..models import Category


def admin_category_view(request):
    '''Displays the category page'''
    return render(request, "insurance/admin_category.html")


def admin_add_category_view(request):
    """Add new category view."""
    categoryForm = forms.CategoryForm()
    if request.method == "POST":
        categoryForm = forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect("admin-view-category")
    return render(
        request, "insurance/admin_add_category.html", {"categoryForm": categoryForm}
    )


def admin_view_category_view(request):
    """Display all category view."""
    categories = models.Category.objects.all()
    return render(
        request, "insurance/admin_view_category.html", {"categories": categories}
    )


def admin_delete_category_view(request):
    '''Display the delete category option'''
    categories = models.Category.objects.all()
    return render(
        request, "insurance/admin_delete_category.html", {"categories": categories}
    )


def delete_category_view(request, pk):
    """Delete category view."""
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("admin-delete-category")


def admin_update_category_view(request):
    '''view to display the update category option'''
    categories = models.Category.objects.all()
    return render(
        request, "insurance/admin_update_category.html", {"categories": categories}
    )


@login_required(login_url="adminlogin")
def update_category_view(request, pk):
    """Update category view."""
    category = models.Category.objects.get(id=pk)
    categoryForm = forms.CategoryForm(instance=category)

    if request.method == "POST":
        categoryForm = forms.CategoryForm(request.POST, instance=category)

        if categoryForm.is_valid():
            categoryForm.save()
            return redirect("admin-update-category")
    return render(
        request, "insurance/update_category.html", {"categoryForm": categoryForm}
    )
    
    

