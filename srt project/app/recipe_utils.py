# recipe_utils.py
import requests

def fetch_themealdb_recipe(dish_name):
    """
    Fetch recipe from TheMealDB API using dish name.
    Returns a dictionary: {"ingredients": [...], "instructions": "..."}
    """
    url = "https://www.themealdb.com/api/json/v1/1/search.php"
    params = {"s": dish_name}

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if not data.get("meals"):
            return {"ingredients": [], "instructions": ""}

        meal = data["meals"][0]

        # --- Ingredients ---
        ingredients = []
        for i in range(1, 21):  # TheMealDB has up to 20 ingredients
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")
            if ingredient and ingredient.strip():
                ingredients.append(f"{measure.strip()} {ingredient.strip()}".strip())

        # --- Instructions ---
        instructions = meal.get("strInstructions", "").strip()

        return {"ingredients": ingredients, "instructions": instructions}

    except Exception as e:
        print(f"Error fetching recipe: {e}")
        return {"ingredients": [], "instructions": ""}
