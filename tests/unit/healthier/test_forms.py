"""
unit tests for Heathier app forms
"""

from unittest import mock

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from healthier.forms import FoodQuery, Login, Signin


class Test_Foodquery_form(TestCase):
    def test_food_query_form_name_label(self):
        form = FoodQuery()
        self.assertTrue(form.fields["name"].label == "name")


class Test_Signin_form(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="coucou@google.com", first_name="Joe", email="wwww@wwww.www"
        )

    def test_signin_form_first_name_label(self):
        form = Signin()
        self.assertTrue(form.fields["first_name"].label == "prénom")

    def test_signin_form_email_label(self):
        form = Signin()
        self.assertTrue(form.fields["email"].label == "email")

    def test_signin_form_save(self):
        form = Signin(
            data={
                "first_name": "Joe",
                "email": "coucou@google.com",
                "password1": "1234567BE89",
                "password2": "1234567BE89",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEquals(
            form.save(),
            {
                "email": [
                    "coucou@google.com est déjà utilisé par un autre compte, merci d'en utiliser un autre"
                ]
            },
        )

        def mock_login_true(*args, **kwargs):
            pass

        def mock_user_save(*args, **kwargs):
            pass

        with mock.patch("django.contrib.auth.models.User.save", new=mock_user_save):
            with mock.patch("healthier.forms.login", new=mock_login_true):
                form = Signin(
                    data={
                        "first_name": "Joe",
                        "email": "erzezevze@google.com",
                        "password1": "1234567BE89",
                        "password2": "1234567BE89",
                    }
                )
                self.assertTrue(form.save())


class Test_Login_form(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="coucou@google.com", first_name="Joe", email="wwww@wwww.www"
        )

    def test_signin_form_first_name_label(self):
        form = Login()
        self.assertTrue(form.fields["username"].label == "email")

    def test_log_user(self):
        form = Login(data={"username": "coucou@google.com", "password": "1234567BE89"})

        def mock_login_Validation_Error(*args, **kwargs):
            return ValidationError("none")

        def mock_clean_pass(*args, **kwargs):
            pass

        with mock.patch("healthier.forms.login", new=mock_login_Validation_Error):
            with mock.patch(
                "django.contrib.auth.forms.AuthenticationForm.clean",
                new=mock_clean_pass,
            ):
                self.assertRaisesMessage(
                    ValidationError,
                    ["E-mail et/ou mot de passe invalides (['none'])"],
                    form.log_user(),
                )
