from django.urls import path

from . import views

app_name = "Management"
urlpatterns = [
    # ex: /Management/login/
    path("login/", views.login, name="login"),
    # /Manegement/logout/
    path("logout/", views.logout, name="logout"),
    # ex: /Management/test/
    path("test/", views.index, name="index"),
    # ex: /Management/test/5
    path("test/view/<int:subjective_test_id>", views.view, name="view"),
    # ex: /Management/test/new/
    path("test/new/", views.new, name="new"),
    # ex: /Management/test/delete/5
    path("test/delete/<int:subjective_test_id>", views.delete, name="delete"),
    # /Management/test/enable/5
    path("test/enable/<int:subjective_test_id>", views.enable, name="enable"),
]
