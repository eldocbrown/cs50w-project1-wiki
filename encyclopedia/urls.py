from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("action/random", views.random, name="random"),
    path("action/newpage", views.newpage, name="newpage"),
    path("action/editpage/<str:entry>", views.editpage, name="editpage"),
    path("message", views.message, name="message"),
]
