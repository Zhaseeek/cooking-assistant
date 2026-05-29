from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('clean_recipes.csv')

recipes = []

for i in range(len(df)):

    ingredients_text = str(df.loc[i, 'ingredients']).lower()

    tags = []

    # HIGH PROTEIN
    if any(word in ingredients_text for word in [
        'chicken',
        'beef',
        'eggs',
        'egg',
        'fish',
        'tuna',
        'salmon',
        'shrimp',
        'turkey',
        'beans',
        'cheese',
        'milk',
        'yogurt'
    ]):

        tags.append('High Protein')

    # VEGETARIAN
    if not any(word in ingredients_text for word in [
        'chicken',
        'beef',
        'fish',
        'salmon',
        'shrimp',
        'turkey',
        'pork',
        'bacon',
        'tuna'
    ]):

        tags.append('Vegetarian')

    # VEGAN
    if not any(word in ingredients_text for word in [
        'chicken',
        'beef',
        'fish',
        'salmon',
        'shrimp',
        'turkey',
        'pork',
        'bacon',
        'tuna',
        'milk',
        'cheese',
        'butter',
        'cream',
        'egg',
        'eggs',
        'yogurt'
    ]):

        tags.append('Vegan')

    # GLUTEN FREE
    if not any(word in ingredients_text for word in [
        'flour',
        'bread',
        'pasta',
        'cake',
        'cookies',
        'wheat',
        'noodles'
    ]):

        tags.append('Gluten Free')

    # SWEET
    if any(word in ingredients_text for word in [
        'sugar',
        'vanilla',
        'chocolate',
        'cookies',
        'cake',
        'cream',
        'banana',
        'cocoa',
        'honey',
        'dessert'
    ]):

        tags.append('Sweet')

    # CALORIES
    if len(ingredients_text) > 500:

        calories = "700 kcal"

    elif len(ingredients_text) > 250:

        calories = "500 kcal"

    else:

        calories = "300 kcal"

    recipes.append({

        "id": i,

        "name": str(df.loc[i, 'clean_title']),

        "ingredients": str(df.loc[i, 'ingredients'])
    .replace('[', '')
    .replace(']', '')
    .replace('"', ''),

        "directions": str(df.loc[i, 'directions'])
    .replace('[', '')
    .replace(']', '')
    .replace('"', ''),

        "tags": tags,

        "calories": calories

    })

@app.route('/')
def home():

    results = []

    limit = request.args.get('limit', 10, type=int)

    user_input = request.args.get('ingredients', '').lower()

    high_protein = request.args.get('high_protein')
    vegetarian = request.args.get('vegetarian')
    vegan = request.args.get('vegan')
    gluten_free = request.args.get('gluten_free')
    low_calorie = request.args.get('low_calorie')
    sweet = request.args.get('sweet')

    if user_input:

        words = user_input.split()

        scored_results = []

        for recipe in recipes:

            ingredients = recipe["ingredients"].lower().split()

            score = 0

            for word in words:

                for ingredient_word in ingredients:

                    if word in ingredient_word:

                        score += 1

            if score > 0:

                recipe_tags = recipe["tags"]

                if high_protein and 'High Protein' not in recipe_tags:
                    continue

                if vegetarian and 'Vegetarian' not in recipe_tags:
                    continue

                if vegan and 'Vegan' not in recipe_tags:
                    continue

                if gluten_free and 'Gluten Free' not in recipe_tags:
                    continue

                if sweet and 'Sweet' not in recipe_tags:
                    continue

                if low_calorie and recipe["calories"] != "300 kcal":
                    continue

                scored_results.append((recipe, score))

        scored_results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        results = [r[0] for r in scored_results[:limit]]

    return render_template(
        'index.html',
        results=results,
        user_input=user_input,
        limit=limit
    )

@app.route('/recipe/<int:recipe_id>')
def recipe_page(recipe_id):

    recipe = recipes[recipe_id]

    current_ingredients = recipe["ingredients"].lower().split()

    similar_recipes = []

    for r in recipes:

        if r["id"] == recipe_id:
            continue

        other_ingredients = r["ingredients"].lower().split()

        similarity_score = 0

        for word in current_ingredients:

            if word in other_ingredients:
                similarity_score += 1

        if similarity_score > 3:

            similar_recipes.append((r, similarity_score))

    similar_recipes.sort(
        key=lambda x: x[1],
        reverse=True
    )

    similar_recipes = [r[0] for r in similar_recipes[:3]]

    return render_template(
        'recipe.html',
        recipe=recipe,
        similar_recipes=similar_recipes
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)