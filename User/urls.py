from django.urls import path

from . import views

app_name = "User"

urlpatterns = [
    # ex: /user/login/
    path("login/", views.login, name="login"),
    # /user/logout/
    path("logout/", views.logout, name="logout"),
    # ex: /user/test/
    path("test/", views.index, name="index"),
    # ex: /user/test/5/
    path("test/<int:subjective_test_id>", views.view, name="view"),
    # ex: /user/test/delete/5/
    path("test/delete/<int:subjective_test_id>", views.delete, name="delete"),
]
