from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
	path("account/register", views.register, name="register"),
	path("account/login", auth_views.LoginView.as_view(), name="login"),
	path("account/logout", auth_views.LogoutView.as_view(), name="logout"),
	path("", views.contact_person_list,
		 name="contact_person_list"),
	path("contact_person/add", views.contact_person_add,
		 name="contact_person_add"),
	path("contact_person/<int:pk>/edit", views.contact_person_edit,
		 name="contact_person_edit"),
	path("contact_person/<int:pk>/delete", views.contact_person_delete,
		 name="contact_person_delete"),
	path("contact_person/import", views.contact_person_import,
		 name="contact_person_import"),
	path("contact_person/export", views.contact_person_export,
		 name="contact_person_export"),

]