from django.test import TestCase
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.models import User
from healthier.models import Food_item, Category


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
    food.categories.add(cat)
    food2.categories.add(cat)
    food3.categories.add(cat)
    food4.categories.add(cat)
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
        self.assertContains(response, 'title="Loggin / Créer un compte"')
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
        response = self.client.get("/moncompte")
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
            response, reverse("healthier:login") + "?next=%2Fmoncompte"
        )


class Test_Purbeurre_healthier_myfoods(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup()

    def test_myfoods_exists_when_logged_in(self):
        self.assertTrue(
            self.client.login(username="google@google.com", password="123456789")
        )
        response = self.client.get("/mesaliments")
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
            response, reverse("healthier:login") + "?next=%2Fmesaliments"
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
        response = self.client.get("/resultats", data={"form": "Chamallows"})
        self.assertEqual(response.status_code, 200)

    def test_results_url_accessible_by_name_when_data(self):
        response = self.client.get(reverse("healthier:results"), data={"form": "Chamallows"})
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
        self.assertTrue(
            self.client.login(username="google@google.fr", password="123456789")
        )
        food_item_id = Food_item.objects.get(name__exact="Orange").id
        response = self.client.post(
                        reverse("healthier:results"),
                        data={"value": food_item_id}
                    )
        self.assertContains(response, "added")
        favorites = Food_item.objects.get(favoris__username="google@google.fr")

    def test_results_when_form_is_valid(self):

            # first case : form is valid and 
            # query returns several items from fooditem name provided items number <100:
            response = self.client.get(
                reverse("healthier:results"),
                data={"form": "form", "name": "Chamallows"},
            )
            self.assertEqual(
                response.context["form"].errors,
                {
                    "__all__": [
                        "Il existe 2"
                        " aliments contenant 'Chamallows' !"
                        " merci de choisir l'aliment à remplacer dans la liste ci dessous."
                    ]
                },
            )
            # second case one item to be replaced is found and 
            # several replacement items are returned:
            response = self.client.get(
                reverse("healthier:results"),
                data={"form": "form", "name": "Citron"},
            )
            self.assertContains(
                response,
                "Orange"
            )
            self.assertContains(
                response,
                "Chamallows mallows"
            )
            self.assertContains(
                response,
                "Citron"
            )
            # third case query does not find a food item from fooditem name provided:
            response = self.client.get(
                reverse("healthier:results"),
                data={"form": "form", "name": "Bar"},
            )
            self.assertEqual(
                response.context["form"].errors,
                {
                    "__all__": [
                        "Bar "
                        "est introuvable dans notre liste d'aliments ! "
                        "Merci de renouveller votre recherche"
                    ]
                },
            )
            # fourth case query does not find any replacement items from the given food name:
            response = self.client.get(
                reverse("healthier:results"),
                data={"form": "form", "name": "Orange"},
            )
            self.assertEqual(
                response.context["form"].errors,
                {
                    "__all__": [
                        "il n'existe pas à ce jour d'aliment de remplacement plus sain dans notre base de données."
                    ]
                },
            )


class Test_Purbeurre_healthier_fooditem(TestCase):


    @classmethod
    def setUpTestData(cls):
        setup()

    def test_food_item_exists(self):
        food =Food_item.objects.get(name="Chamallows")
        food_id = food.id
        response = self.client.get(reverse("healthier:fooditem"), data={"food_id":food_id})
        self.assertEqual(response.status_code, 200)

    def test_food_item_url_accessible_by_name(self):
        food =Food_item.objects.get(name="Chamallows")
        food_id = food.id
        response = self.client.get(reverse("healthier:fooditem"), data={"food_id":food_id})
        self.assertEqual(response.status_code, 200)

    def test_food_uses_correct_template(self):
        food =Food_item.objects.get(name="Chamallows")
        food_id = food.id
        response = self.client.get(reverse("healthier:fooditem"), data={"food_id":food_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'healthier/_food_item.html')
    
    def test_fomr1_in_response(self):
        food =Food_item.objects.get(name="Chamallows")
        food_id = food.id
        response = self.client.get(reverse("healthier:fooditem"), data={"food_id":food_id})
        self.assertContains(response, "form1")

    def test_food_item_is_returned_when_found(self):
        food =Food_item.objects.get(name="Chamallows")
        food_id = food.id
        response = self.client.get(reverse("healthier:fooditem"), data={"food_id":food_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["food_item"], Food_item.objects.get(id=food_id) )

    def test_404_is_returned_when_not_found(self):
        response = self.client.get(reverse("healthier:fooditem"), data={"food_id":18})
        self.assertEqual(response.status_code, 404)


class Test_Purbeurre_healthier_login(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup()

    def test_tries_to_log_in_when_GET_data(self):
        response = self.client.get(
            reverse("healthier:login"),
            data={"username":"google@google.com", "password":"123456789"},
        )
        self.assertRedirects(
            response,
            reverse("healthier:myaccount"),
        )
    def test_error_wrong_credentials(self):
        response = self.client.get(
            reverse("healthier:login"),
            data={"username":"BAR", "password":"123456789"}
        )
        self.assertTrue("modaltoshow" in response.context)

    def test_logout_and_redirects_when_user_logged_in(self):
        self.assertTrue(
            self.client.login(
                username="google@google.com",
                password="123456789"
                )
        )
        response = self.client.get(reverse("healthier:login"))
        self.assertRedirects(response, reverse("healthier:home"))

    def test_save_new_user_and_redirects(self):
        # user created and logged in
        response = self.client.post(
                        reverse("healthier:login"),
                        data={
                            "email":"cccsdf@guggle.fra",
                            "first_name" : "pppp",
                            "password1": "randompassword35",
                            "password2": "randompassword35",
                        }
                    )
        self.assertRedirects(
            response,
            reverse("healthier:myaccount"),
        )
        user = User.objects.get(username="cccsdf@guggle.fra")
        self.assertEqual(user.email, "cccsdf@guggle.fra")
        self.assertEqual(user.first_name, "pppp")

    def test_NOT_save_new_user(self):
        response = self.client.post(
                        reverse("healthier:login"),
                        data={
                            "email":"cccsdgugglefra",
                            "first_name" : "pppp",
                            "password1": "randompassword35",
                            "password2": "randompassword35",
                        }
                    )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("modaltoshow" in response.context)
        self.assertTrue("sign_form" in response.context)
        
        

