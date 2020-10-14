from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("random", views.random, name="random"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage/<str:entry>", views.editpage, name="editpage"),
    path("message", views.message, name="message"),
]
