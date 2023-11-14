from django.urls import path
from insurance.views import views
from django.contrib.auth.views import LogoutView, LoginView
from .views import category, constants, customers, policy, questions


urlpatterns = [
    path("", views.home_view, name=""),
    path(
        "logout",
        LogoutView.as_view(template_name="insurance/logout.html"),
        name="logout",
    ),
    path("aboutus", constants.aboutus_view),
    path("contactus", constants.contactus_view),
    path("afterlogin", views.afterlogin_view, name="afterlogin"),
    path(
        "adminlogin",
        LoginView.as_view(template_name="insurance/adminlogin.html"),
        name="adminlogin",
    ),
    path("admin-dashboard", views.admin_dashboard_view, name="admin-dashboard"),
    path(
        "admin-view-customer",
        customers.admin_view_customer_view,
        name="admin-view-customer",
    ),
    path(
        "update-customer/<int:pk>",
        customers.update_customer_view,
        name="update-customer",
    ),
    path(
        "delete-customer/<int:pk>",
        customers.delete_customer_view,
        name="delete-customer",
    ),
    path("admin-category", category.admin_category_view, name="admin-category"),
    path(
        "admin-view-category",
        category.admin_view_category_view,
        name="admin-view-category",
    ),
    path(
        "admin-update-category",
        category.admin_update_category_view,
        name="admin-update-category",
    ),
    path(
        "update-category/<int:pk>",
        category.update_category_view,
        name="update-category",
    ),
    path(
        "admin-add-category",
        category.admin_add_category_view,
        name="admin-add-category",
    ),
    path(
        "admin-delete-category",
        category.admin_delete_category_view,
        name="admin-delete-category",
    ),
    path(
        "delete-category/<int:pk>",
        category.delete_category_view,
        name="delete-category",
    ),
    path("admin-policy", policy.admin_policy_view, name="admin-policy"),
    path("admin-add-policy", policy.admin_add_policy_view, name="admin-add-policy"),
    path("admin-view-policy", policy.admin_view_policy_view, name="admin-view-policy"),
    path(
        "admin-update-policy",
        policy.admin_update_policy_view,
        name="admin-update-policy",
    ),
    path("update-policy/<int:pk>", policy.update_policy_view, name="update-policy"),
    path(
        "admin-delete-policy",
        policy.admin_delete_policy_view,
        name="admin-delete-policy",
    ),
    path("delete-policy/<int:pk>", policy.delete_policy_view, name="delete-policy"),
    path(
        "admin-view-policy-holder",
        policy.admin_view_policy_holder_view,
        name="admin-view-policy-holder",
    ),
    path(
        "admin-view-approved-policy-holder",
        policy.admin_view_approved_policy_holder_view,
        name="admin-view-approved-policy-holder",
    ),
    path(
        "admin-view-disapproved-policy-holder",
        policy.admin_view_disapproved_policy_holder_view,
        name="admin-view-disapproved-policy-holder",
    ),
    path(
        "admin-view-waiting-policy-holder",
        policy.admin_view_waiting_policy_holder_view,
        name="admin-view-waiting-policy-holder",
    ),
    path(
        "approve-request/<int:pk>", policy.approve_request_view, name="approve-request"
    ),
    path(
        "reject-request/<int:pk>", policy.disapprove_request_view, name="reject-request"
    ),
    path("admin-question", questions.admin_question_view, name="admin-question"),
    path(
        "update-question/<int:pk>",
        questions.update_question_view,
        name="update-question",
    ),
]
