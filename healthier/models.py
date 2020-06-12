"""
Healthier app models
"""

from random import choice

from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models


class Store(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Food_item(models.Model):

    open_food_facts_url = models.URLField(max_length=400)
    name = models.CharField(max_length=200)
    energy_100g = models.CharField(max_length=20)
    nutri_score_fr = models.CharField(
        max_length=1, choices=[("a", "a"), ("b", "b"), ("c", "c"), ("d", "d")]
    )
    nova_grade = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])
    image_url = models.URLField(max_length=400)
    id_open_food_facts = models.BigIntegerField(unique=True)
    stores = models.ManyToManyField(Store)
    brands = models.ManyToManyField(Brand)
    categories = models.ManyToManyField(Category)
    favoris = models.ManyToManyField(User)
    image_nutrition_url = models.URLField(max_length=400)

    def __str__(self):
        return self.name

    @staticmethod
    def get_favorites(username):
        favorites = Food_item.objects.filter(favoris__username=username)
        if favorites.exists():
            return favorites
        else:
            return False

    @staticmethod
    def save_favorites(food_id, user):
        """ 
        Adds a favoris relation between food_id:<INT> and user:<User object>
        returns a dict in any case, the key "status" is set to True only on succesful transaction
        """
        try:
            f = Food_item.objects.get(id=food_id)
            f.favoris.get(username=user.username)
            return {"result": "already existing", "status": False}
        except ObjectDoesNotExist:
            try:
                f.favoris.add(user)
                return {"result": "added", "status": True}
            except:
                return {"result": "unforeseen exception", "status": False}
        else:
            return {"result": "unforeseen exception", "status": False}

    @staticmethod
    def get_searched_food_Item(food_name=None, food_id=None):
        """
        Takes either food_name:<STR> or food_id:<INT>, returns a <dict> :
        {
            "status": "choice_to_make" or "not_found, or "ok" or "no_replacement",
            "replacement_items": None or <Queryset>,
            "to_be_replaced_item": Food_item object or <Queryset> or None
        }

        First tries to find a Food_item object with self.search() or get() depending on given arguments
        if more than one or None are found returns with a dict.

        if one result is found, a call is made to self.replace() without arguments
        if healthier replacements are found a dict is returned,
        else a second call to self.replace is made with the argt nutri-only (less restrictive) and a dict
        is returned with or without results.
        """
        if food_id == None:
            Items_found, number_items_found = Food_item.search(food_name)
            if number_items_found == 1:
                if type(Items_found) == models.QuerySet:
                    Items_found = list(Items_found)[0]
            elif number_items_found > 1:
                return {
                    "status": "choice_to_make",
                    "replacement_items": None,
                    "to_be_replaced_item": Items_found,
                }
            else:
                return {
                    "status": "not_found",
                    "replacement_items": None,
                    "to_be_replaced_item": None,
                }
        else:
            Items_found = Food_item.objects.get(id=food_id)

        replacement = Food_item.replace(Items_found)
        if replacement[0] == True:
            return {
                "status": "ok",
                "replacement_items": replacement[1],
                "to_be_replaced_item": Items_found,
            }
        else:
            replacement = Food_item.replace(Items_found, status="nutri-only")
            if replacement[0] == True:
                return {
                    "status": "ok",
                    "replacement_items": replacement[1],
                    "to_be_replaced_item": Items_found,
                }
            else:
                return {
                    "status": "no_replacement",
                    "replacement_items": None,
                    "to_be_replaced_item": Items_found,
                }

    @staticmethod
    def search(food_name):
        """ 
        Takes food_name:<STR> returns a Tuple (<Queryset> or Food_item object, number of items found)
        Searches through the DB if food_name exists among Food_items names.
        """
        try:
            f = Food_item.objects.get(name__icontains=food_name)
            return (f, 1)
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            f = (
                Food_item.objects.filter(name__icontains=food_name)
                .order_by("name")
                .distinct("name")
            )
            return (f, f.all().count())

    @staticmethod
    def replace(food_item, status=None):
        """
        Takes foo_item:<foo_item object> and status:<STR> returns a Tuple(True or False, <Queryset> or None)
        the tuple is True when "healthier"* replacements food_item are found having as much as possible identical
        categories as food_item.categories.

        *"healthier" means in this case :
            - if status=None, the food items returned will have both better (inferior) nutri-score and Nova-grade
            - is stauts=nutry-only, the food items returnes will have only a better (inferior) nutri-score.

        Due to the variable number and order of foo_item.categories the function gets the food_items present
        in DB in a <Queryset> for each category converts it into set() and use intersect() two times in a row
        to find food_items that have the most categories in common with food_item.
        """
        categories = list(food_item.categories.all())
        if status == None:
            replacements = {
                Food_item.objects.filter(
                    categories__name=category,
                    nutri_score_fr__lt=food_item.nutri_score_fr,
                    nova_grade__lt=food_item.nova_grade,
                ).order_by(
                    "nutri_score_fr", "nova_grade",
                )
                for category in categories
            }
        elif status == "nutri-only":
            replacements = {
                Food_item.objects.filter(
                    categories__name=category,
                    nutri_score_fr__lt=food_item.nutri_score_fr,
                ).order_by("nutri_score_fr", "nova_grade")
                for category in categories
            }
        query = []
        {
            query.append(replacement)
            for replacement in replacements
            if replacement.exists()
        }
        cat_number = len(query)
        results = []
        if cat_number > 0:
            replacement_foods = query[0]
            if cat_number > 1:
                i = 0
                while i < cat_number - 2:
                    intersect = query[i].intersection(query[i + 1])
                    if intersect.exists():
                        results.append(intersect)
                    i += 1
                if len(results) > 0:
                    replacement_foods = results[0]
                    x = 0
                    results_choices = []
                    if len(results) > 1:
                        while x < len(results) - 2:
                            result = results[x].intersection(results[x + 1])
                            if result.exists():
                                results_choices.append(result)
                            x += 1
                        if len(results_choices) > 0:
                            replacement_foods = choice(results_choices)
                            return (True, replacement_foods)
                        else:
                            return (True, replacement_foods)
                    else:
                        return (True, replacement_foods)
                else:
                    return (True, replacement_foods)
            else:
                return (True, replacement_foods)
        else:
            return (False, None)
