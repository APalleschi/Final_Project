from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.welcome, name="welcome"),
    path("index", views.index, name="index"),
    path("sections", views.sections, name="sections"),
    path("sections/<int:section_id>", views.section, name="section"),
    path("create", views.create, name="create"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    # path("listings/<int:listing_id>/comment", views.comment, name="comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("users/<int:user_id>", views.profile, name="profile"),
    path("loan", views.loan, name="loan"),
    path("loan/add", views.loan_add, name="loan_add"),
    path("loan/delete", views.loan_delete, name="loan_delete"),
    path("restricted", views.restricted, name="restricted")

]
