from django.urls import path
from insurance.views import *
from django.contrib.auth.views import LogoutView, LoginView
from .views import category_views, base_views, customer_views, policy_views, questions_views,dashboard


urlpatterns = [
    path("", dashboard.home_view, name=""),
    path(
        "logout",
        LogoutView.as_view(template_name="insurance/logout.html"),
        name="logout",
    ),
    path("aboutus", base_views.aboutus_view),
    path("contactus", base_views.contactus_view),
    path("afterlogin", dashboard.afterlogin_view, name="afterlogin"),
    path(
        "adminlogin",
        LoginView.as_view(template_name="insurance/adminlogin.html"),
        name="adminlogin",
    ),
    path("admin-dashboard", dashboard.admin_dashboard_view, name="admin-dashboard"),
    path(
        "admin-view-customer",
        customer_views.admin_view_customer_view,
        name="admin-view-customer",
    ),
    path(
        "update-customer/<int:pk>",
        customer_views.update_customer_view,
        name="update-customer",
    ),
    path(
        "delete-customer/<int:pk>",
        customer_views.delete_customer_view,
        name="delete-customer",
    ),
    path("admin-category", category_views.admin_category_view, name="admin-category"),
    path(
        "admin-view-category",
        category_views.admin_view_category_view,
        name="admin-view-category",
    ),
    path(
        "admin-update-category",
        category_views.admin_update_category_view,
        name="admin-update-category",
    ),
    path(
        "update-category/<int:pk>",
        category_views.update_category_view,
        name="update-category",
    ),
    path(
        "admin-add-category",
        category_views.admin_add_category_view,
        name="admin-add-category",
    ),
    path(
        "admin-delete-category",
        category_views.admin_delete_category_view,
        name="admin-delete-category",
    ),
    path(
        "delete-category/<int:pk>",
        category_views.delete_category_view,
        name="delete-category",
    ),
    path("admin-policy", policy_views.admin_policy_view, name="admin-policy"),
    path("admin-add-policy", policy_views.admin_add_policy_view, name="admin-add-policy"),
    path("admin-view-policy", policy_views.admin_view_policy_view, name="admin-view-policy"),
    path(
        "admin-update-policy",
        policy_views.admin_update_policy_view,
        name="admin-update-policy",
    ),
    path("update-policy/<int:pk>", policy_views.update_policy_view, name="update-policy"),
    path(
        "admin-delete-policy",
        policy_views.admin_delete_policy_view,
        name="admin-delete-policy",
    ),
    path("delete-policy/<int:pk>", policy_views.delete_policy_view, name="delete-policy"),
    path(
        "admin-view-policy-holder",
        policy_views.admin_view_policy_holder_view,
        name="admin-view-policy-holder",
    ),
    path(
        "admin-view-approved-policy-holder",
        policy_views.admin_view_approved_policy_holder_view,
        name="admin-view-approved-policy-holder",
    ),
    path(
        "admin-view-disapproved-policy-holder",
        policy_views.admin_view_disapproved_policy_holder_view,
        name="admin-view-disapproved-policy-holder",
    ),
    path(
        "admin-view-waiting-policy-holder",
        policy_views.admin_view_waiting_policy_holder_view,
        name="admin-view-waiting-policy-holder",
    ),
    path(
        "approve-request/<int:pk>", policy_views.approve_request_view, name="approve-request"
    ),
    path(
        "reject-request/<int:pk>", policy_views.disapprove_request_view, name="reject-request"
    ),
    path("admin-question", questions_views.admin_question_view, name="admin-question"),
    path(
        "update-question/<int:pk>",
        questions_views.update_question_view,
        name="update-question",
    ),
]
