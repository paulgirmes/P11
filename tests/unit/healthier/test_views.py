"""
unit tests for Heathier app views
"""

from unittest import mock

from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase
from django.urls import reverse

from healthier.models import Category, Food_item


def setup():
    testuser = User.objects.create_user(
        "google@google.com",
        email="google@google.com",
        password="123456789",
        first_name="Joe",
    )
    testuser2 = User.objects.create_user(
        "google@google.fr",
        email="google@google.fr",
        password="123456789",
        first_name="Joe",
    )
    food = Food_item.objects.create(
        open_food_facts_url="https://fr.openfoodfacts.org/produit/3103220009512/chamallows-haribo",
        name="Chamallows",
        nutri_score_fr="d",
        nova_grade=3,
        image_url="https://static.openfoodfacts.org/images/products/310/322/000/9512/front_fr.54.400.jpg",
        id_open_food_facts="1",
        energy_100g="326kcal",
        image_nutrition_url="326kcal",
    )
    food2 = Food_item.objects.create(
        open_food_facts_url="https://fr.openfoodfacts.org/produit/3103220009512/chamallows-haribo",
        name="Chamallows mallows",
        nutri_score_fr="a",
        nova_grade=2,
        image_url="https://static.openfoodfacts.org/images/products/310/322/000/9512/front_fr.54.400.jpg",
        id_open_food_facts="2",
        energy_100g="326kcal",
        image_nutrition_url="326kcal",
    )
    food3 = Food_item.objects.create(
        open_food_facts_url="https://fr.openfoodfacts.org/produit/3103220009512/chamallows-haribo",
        name="Citron",
        nutri_score_fr="b",
        nova_grade="3",
        image_url="https://static.openfoodfacts.org/images/products/310/322/000/9512/front_fr.54.400.jpg",
        id_open_food_facts="3",
        energy_100g="326kcal",
        image_nutrition_url="326kcal",
    )
    food4 = Food_item.objects.create(
        open_food_facts_url="https://fr.openfoodfacts.org/produit/3103220009512/chamallows-haribo",
        name="Orange",
        nutri_score_fr="a",
        nova_grade="1",
        image_url="https://static.openfoodfacts.org/images/products/310/322/000/9512/front_fr.54.400.jpg",
        id_open_food_facts="4",
        energy_100g="326kcal",
        image_nutrition_url="326kcal",
    )
    cat = Category.objects.create(name="bonbons")
    cat1 = Category.objects.create(name="fruits")
    cats = [cat, cat1]
    foods = [food, food2, food3, food4]
    {food.categories.add(cat) for food in foods for cat in cats}
    food.favoris.add(testuser)


class Test_purbeurre_urls(TestCase):
    def test_admin_exists(self):
        response = self.client.get("/admin/")
        self.assertRedirects(response, "/admin/login/?next=%2Fadmin%2F")

    def test_admin_url_accessible_by_name(self):
        response = self.client.get(reverse("admin:login"))
        self.assertEqual(response.status_code, 200)


class Test_Purbeurre_healthier_home(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup()

    def test_home_exists(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_home_url_accessible_by_name(self):
        response = self.client.get(reverse("healthier:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        response = self.client.get(reverse("healthier:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_index.html")

    def test_home_data_privacy_modal_not_logged_in(self):
        response = self.client.get(reverse("healthier:home"))
        self.assertContains(response, "modal fade")
        # check that modal is not in response when session cookie is set by an other view
        self.client.get(reverse("healthier:contact"))
        response = self.client.get(reverse("healthier:home"))
        self.assertNotContains(response, "modal fade")

    def test_home_data_privacy_modal_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("healthier:home"))
        self.assertNotContains(response, "modal fade")

    def test_home_nav_header_not_logged_in(self):
        response = self.client.get(reverse("healthier:home"))
        self.assertContains(response, 'title="Login / Créer un compte"')
        self.assertNotContains(response, 'title="Mon Compte"')

    def test_home_nav_header_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("healthier:home"))
        self.assertNotContains(response, 'title="Loggin / Créer un compte"')
        self.assertContains(response, 'title="Mon Compte"')

    def test_home_forms_exists(self):
        response = self.client.get(reverse("healthier:home"))
        self.assertTrue("form" in response.context)
        self.assertTrue("form1" in response.context)


class Test_Purbeurre_healthier_myaccount(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup()

    def test_myaccount_exists_when_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get("/moncompte/")
        self.assertEqual(response.status_code, 200)

    def test_myaccount_url_accessible_by_name_when_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("healthier:myaccount"))
        self.assertEqual(response.status_code, 200)

    def test_myaccount_uses_correct_template_when_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("healthier:myaccount"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_user_page.html")

    def test_myaccount_returns_context_when_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("healthier:myaccount"))
        self.assertTrue("form" in response.context)
        self.assertTrue("user_name" in response.context)
        self.assertTrue("Joe" == response.context["user_name"])
        self.assertTrue("user_mail" in response.context)
        self.assertTrue("google@google.com" == response.context["user_mail"])

    def test_myaccount_redirects_when_not_logged_in(self):
        response = self.client.get(reverse("healthier:myaccount"))
        self.assertRedirects(
            response, reverse("healthier:login") + "?next=%2Fmoncompte/"
        )


class Test_Purbeurre_healthier_myfoods(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup()

    def test_myfoods_exists_when_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get("/mesaliments/")
        self.assertEqual(response.status_code, 200)

    def test_myfoods_url_accessible_by_name_when_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("healthier:myfoods"))
        self.assertEqual(response.status_code, 200)

    def test_myfoods_uses_correct_template_when_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("healthier:myfoods"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_my_saved_foods.html")

    def test_myfoods_redirects_when_not_logged_in(self):
        response = self.client.get(reverse("healthier:myfoods"))
        self.assertRedirects(
            response, reverse("healthier:login") + "?next=%2Fmesaliments/"
        )

    def test_my_food_response_has_content_when_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("healthier:myfoods"))
        self.assertTrue("form1" in response.context)
        self.assertTrue("food_items" in response.context)
        self.assertContains(response, "Chamallows")


class Test_Purbeurre_healthier_results(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup()

    def test_results_url_exists_when_data(self):
        response = self.client.get("/resultats/", data={"form": "Chamallows"})
        self.assertEqual(response.status_code, 200)

    def test_results_url_accessible_by_name_when_data(self):
        response = self.client.get(
            reverse("healthier:results"), data={"form": "Chamallows"}
        )
        self.assertEqual(response.status_code, 200)

    def test_results_uses_correct_template_when_no_results(self):
        response = self.client.get(reverse("healthier:results"), data={"form": 18})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_no_results.html")

    def test_results_uses_correct_template_when_result(self):
        food_item_id = Food_item.objects.get(name__exact="Chamallows").id
        response = self.client.get(reverse("healthier:results"), {"id": food_item_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_results.html")

    def test_results_raises_404_when_no_data(self):
        response = self.client.get(reverse("healthier:results"))
        self.assertEqual(response.status_code, 404)

    def test_results_forms_invalid_field_error(self):
        data = 201 * "x"
        response = self.client.get(
            reverse("healthier:results"), data={"form": "form", "name": data}
        )
        self.assertEqual(
            response.context["form"].errors,
            {
                "name": [
                    "Assurez-vous que cette valeur comporte au plus 200 caractères (actuellement 201)."
                ]
            },
        )
        response = self.client.get(
            reverse("healthier:results"), data={"form1": "form", "name": data}
        )
        self.assertEqual(
            response.context["form"].errors,
            {
                "name": [
                    "Assurez-vous que cette valeur comporte au plus 200 caractères (actuellement 201)."
                ]
            },
        )

    def test_results_returns_result_when_POST(self):
        def mock_Food_item_save_favorites(self, *args, **kwargs):
            return {"result": "added", "status": True}

        with mock.patch(
            "healthier.views.Food_item.save_favorites",
            new=mock_Food_item_save_favorites,
        ):
            response = self.client.post(
                reverse("healthier:results"), data={"value": "XXXXXX"}
            )
            self.assertContains(response, "added")

    def test_results_when_form_is_valid(self):

        # workaround to mock <queryset>.count() method
        # used on results["to_be_replaced_items"] in views.results :
        class Queryset(list):
            def __init__(self, number=0):
                self.number = number

            def count(self):
                return self.number

        def mock_Food_item_get_searched_food_Item(food_id=None, food_name=None):
            if food_name == "OK":
                return {
                    "status": "ok",
                    "replacement_items": "several",
                    "to_be_replaced_item": "one",
                }
            if food_name == "choice_to_make":
                return {
                    "status": "choice_to_make",
                    "replacement_items": "none",
                    "to_be_replaced_item": Queryset(99),
                }
            if food_name == "choice_to_make>100":
                return {
                    "status": "choice_to_make",
                    "replacement_items": "several",
                    "to_be_replaced_item": Queryset(101),
                }
            if food_name == "not_found":
                return {
                    "status": "not_found",
                    "replacement_items": "none",
                    "to_be_replaced_item": "one",
                }
            if food_name == "no_replacement":
                return {
                    "status": "no_replacement",
                    "replacement_items": "none",
                    "to_be_replaced_item": "one",
                }

        with mock.patch(
            "healthier.views.Food_item.get_searched_food_Item",
            new=mock_Food_item_get_searched_food_Item,
        ):
            # first case : form is valid and
            # query returns several items from fooditem name provided items number <100:
            response = self.client.get(
                reverse("healthier:results"),
                data={"form": "form", "name": "choice_to_make"},
            )
            self.assertEqual(
                response.context["form"].errors,
                {
                    "__all__": [
                        "Il existe 99"
                        " aliments contenant 'choice_to_make' !"
                        " merci de choisir l'aliment à remplacer dans la liste ci dessous."
                    ]
                },
            )
            # second case one item to be replaced is found and
            # several replacement items are returned:
            response = self.client.get(
                reverse("healthier:results"), data={"form": "form", "name": "OK"},
            )
            self.assertEqual(response.context["food_items"], "several")
            self.assertEqual(response.context["searched"], "one")
            # third case query returns several items from fooditem name provided
            # items number >100:
            response = self.client.get(
                reverse("healthier:results"),
                data={"form": "form", "name": "choice_to_make>100"},
            )
            self.assertEqual(
                response.context["form"].errors,
                {
                    "__all__": [
                        "Il existe 101"
                        " aliments contenant 'choice_to_make>100' !"
                        " merci de préciser votre recherche."
                    ]
                },
            )
            # fourth case query does not find a food item from fooditem name provided:
            response = self.client.get(
                reverse("healthier:results"),
                data={"form": "form", "name": "not_found"},
            )
            self.assertEqual(
                response.context["form"].errors,
                {
                    "__all__": [
                        "not_found "
                        "est introuvable dans notre liste d'aliments ! "
                        "Merci de renouveller votre recherche"
                    ]
                },
            )
            # fith case query does not find any replacement items from the given food name:
            response = self.client.get(
                reverse("healthier:results"),
                data={"form": "form", "name": "no_replacement"},
            )
            self.assertEqual(
                response.context["form"].errors,
                {
                    "__all__": [
                        "il n'existe pas à ce jour d'aliment de remplacement plus sain dans notre base de données."
                    ]
                },
            )


class Test_Purbeurre_healthier_contact(TestCase):
    def test_contact_exists(self):
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_contact_url_accessible_by_name(self):
        response = self.client.get(reverse("healthier:contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_uses_correct_template(self):
        response = self.client.get(reverse("healthier:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_contact.html")

    def test_fomr1_in_response(self):
        response = self.client.get(reverse("healthier:contact"))
        self.assertContains(response, "form1")


class Test_Purbeurre_healthier_general_conditions(TestCase):
    def test_general_conditions_exists(self):
        response = self.client.get("/mentions_legales/")
        self.assertEqual(response.status_code, 200)

    def test_general_conditions_url_accessible_by_name(self):
        response = self.client.get(reverse("healthier:general_conditions"))
        self.assertEqual(response.status_code, 200)

    def test_general_uses_correct_template(self):
        response = self.client.get(reverse("healthier:general_conditions"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_legal_content.html")

    def test_fomr1_in_response(self):
        response = self.client.get(reverse("healthier:general_conditions"))
        self.assertContains(response, "form1")


class Test_Purbeurre_healthier_fooditem(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup()

    def test_food_item_exists(self):
        food = Food_item.objects.get(name="Chamallows")
        food_id = food.id
        response = self.client.get(
            reverse("healthier:fooditem"), data={"food_id": food_id}
        )
        self.assertEqual(response.status_code, 200)

    def test_food_item_url_accessible_by_name(self):
        food = Food_item.objects.get(name="Chamallows")
        food_id = food.id
        response = self.client.get(
            reverse("healthier:fooditem"), data={"food_id": food_id}
        )
        self.assertEqual(response.status_code, 200)

    def test_food_uses_correct_template(self):
        food = Food_item.objects.get(name="Chamallows")
        food_id = food.id
        response = self.client.get(
            reverse("healthier:fooditem"), data={"food_id": food_id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_food_item.html")

    def test_fomr1_in_response(self):
        food = Food_item.objects.get(name="Chamallows")
        food_id = food.id
        response = self.client.get(
            reverse("healthier:fooditem"), data={"food_id": food_id}
        )
        self.assertContains(response, "form1")

    def test_food_item_is_returned_when_found(self):
        food = Food_item.objects.get(name="Chamallows")
        food_id = food.id
        response = self.client.get(
            reverse("healthier:fooditem"), data={"food_id": food_id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["food_item"], Food_item.objects.get(id=food_id)
        )

    def test_404_is_returned_when_not_found(self):
        response = self.client.get(reverse("healthier:fooditem"), data={"food_id": 18})
        self.assertEqual(response.status_code, 404)


class Test_Purbeurre_healthier_login(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup()

    def test_login_exists(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_url_accessible_by_name(self):
        response = self.client.get(reverse("healthier:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_uses_correct_template(self):
        response = self.client.get(reverse("healthier:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_login_signin.html")

    def test_GET_context_if_not_logged_in(self):
        response = self.client.get(reverse("healthier:login"))
        self.assertTrue("form1" in response.context)
        self.assertTrue("sign_form" in response.context)
        self.assertTrue("log_form" in response.context)

    def test_tries_to_log_in_when_GET_data(self):
        def mock_login_user_fail(*args, **kwargs):
            raise TypeError

        def mock_login_user_OK(*args, **kwargs):
            return

        with mock.patch("healthier.forms.Login.log_user", new=mock_login_user_OK):
            response = self.client.get(
                reverse("healthier:login"), data={"username": "joe"},
            )
            self.assertRedirects(
                response, reverse("healthier:myaccount"), target_status_code=302,
            )

        with mock.patch("healthier.forms.Login.log_user", new=mock_login_user_fail):
            response = self.client.get(
                reverse("healthier:login"), data={"username": "bar"}
            )
            self.assertTrue("modaltoshow" in response.context)

    def test_logout_and_redirects_when_user_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("healthier:login"))
        self.assertRedirects(response, reverse("healthier:home"))

    def test_save_new_user_and_redirects(self):
        def mock_save_ok(*args, **kwargs):
            return True

        def mock_save_nok(*args, **kwargs):
            return False

        def mock_save_exception(*args, **kwargs):
            raise TypeError

        with mock.patch("healthier.forms.Signin.save", new=mock_save_ok):
            response = self.client.post(
                reverse("healthier:login"),
                data={
                    "email": "cccsdf@guggle.fra",
                    "name": "pppp",
                    "password1": "123456789",
                    "password2": "123456789",
                },
            )
            self.assertRedirects(
                response, reverse("healthier:myaccount"), target_status_code=302
            )
        with mock.patch("healthier.forms.Signin.save", new=mock_save_nok):
            response = self.client.post(
                reverse("healthier:login"),
                data={
                    "email": "cccsdf@guggle.fra",
                    "name": "pppp",
                    "password1": "123456789",
                    "password2": "123456789",
                },
            )
            self.assertTrue("modaltoshow" in response.context)
            self.assertTrue("sign_form" in response.context)
        with mock.patch("healthier.forms.Signin.save", new=mock_save_exception):
            response = self.client.post(
                reverse("healthier:login"),
                data={
                    "email": "cccsdf@guggle.fra",
                    "name": "pppp",
                    "password1": "123456789",
                    "password2": "123456789",
                },
            )
            self.assertEqual(response.status_code, 500)


class Test_Purbeurre_healthier_reset_password(TestCase):
    def test_reset_password_exists(self):
        response = self.client.get("/reset_mdp/")
        self.assertEqual(response.status_code, 200)

    def test_reset_password_url_accessible_by_name(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)

    def test_reset_password_uses_correct_template(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_reset-password.html")

    def test_fomr1_in_response(self):
        response = self.client.get(reverse("password_reset"))
        self.assertContains(response, "form1")

    def test_form_in_response(self):
        response = self.client.get(
            reverse("password_reset_confirm", args=("uidb64", "token"))
        )
        self.assertContains(response, "form")


class Test_Purbeurre_healthier_password_reset_confirm(TestCase):
    def test_password_reset_confirm_exists(self):
        response = self.client.get("/reset_mdp/<uidb64>/<token>/")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirm_url_accessible_by_name(self):
        response = self.client.get(
            reverse("password_reset_confirm", args=("uidb64", "token"))
        )
        self.assertEqual(response.status_code, 200)

    def test_reset_password_uses_correct_template(self):
        response = self.client.get(
            reverse("password_reset_confirm", args=("uidb64", "token"))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_password_reset_confirm.html")

    def test_fomr1_in_response(self):
        response = self.client.get(
            reverse("password_reset_confirm", args=("uidb64", "token"))
        )
        self.assertContains(response, "form1")

    def test_form_in_response(self):
        response = self.client.get(
            reverse("password_reset_confirm", args=("uidb64", "token"))
        )
        self.assertContains(response, "form")


class Test_Purbeurre_healthier_password_reset_done(TestCase):
    def test_password_reset_done_exists(self):
        response = self.client.get("/reset_mdp/ok/")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_url_accessible_by_name(self):
        response = self.client.get(reverse("password_reset_done"))
        self.assertEqual(response.status_code, 200)

    def test_reset_password_uses_correct_template(self):
        response = self.client.get(reverse("password_reset_done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_password_reset_done.html")

    def test_fomr1_in_response(self):
        response = self.client.get(reverse("password_reset_done"))
        self.assertContains(response, "form1")


class Test_Purbeurre_password_reset_complete(TestCase):
    def test_password_reset_complete_exists(self):
        response = self.client.get("/reset_mdp_effectue/")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_url_accessible_by_name(self):
        response = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(response.status_code, 200)

    def test_reset_password_uses_correct_template(self):
        response = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_password_reset_complete.html")

    def test_fomr1_in_response(self):
        response = self.client.get(reverse("password_reset_complete"))
        self.assertContains(response, "form1")


class Test_Purbeurre_password_change(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup()

    def test_password_change_exists(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get("/changement_mdp/")
        self.assertEqual(response.status_code, 200)

    def test_password_change_url_accessible_by_name(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("password_change"))
        self.assertEqual(response.status_code, 200)

    def test_password_change_uses_correct_template(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("password_change"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_password_change.html")

    def test_fomr1_in_response(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("password_change"))
        self.assertContains(response, "form1")


class Test_Purbeurre_password_change_done(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup()

    def test_password_change_done_exists(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get("/changement_mdp/ok/")
        self.assertEqual(response.status_code, 200)

    def test_password_change_done_url_accessible_by_name(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("password_change_done"))
        self.assertEqual(response.status_code, 200)

    def test_password_change_done_uses_correct_template(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("password_change_done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "healthier/_password_change_done.html")

    def test_fomr1_in_response(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get(reverse("password_change"))
        self.assertContains(response, "form1")


class Test_Purbeurre_custom_error_views(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup()

    def test_custom_404_view_exists(self):
        response = self.client.get("/xyz/")
        self.assertContains(response, "form1", status_code=404)

    def test_custom_500_view_exists(self):
        self.client.raise_request_exception = False
        response = self.client.get("/resultats/?id=68596849849zzefgze")
        self.assertContains(response, "form1", status_code=500)
