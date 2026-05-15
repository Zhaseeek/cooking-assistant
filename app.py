from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('clean_recipes.csv')

recipes = []

for i in range(len(df)):
    recipes.append({
        "name": df.loc[i, 'clean_title'],
        "ingredients": df.loc[i, 'clean_ingredients']
    })

@app.route('/')
def home():

    results = []

    user_input = request.args.get('ingredients', '').lower()

    if user_input:

        words = user_input.split()

        scored_results = []

        for recipe in recipes:

            ingredients = recipe["ingredients"].split()

            score = 0

            for word in words:
                if word in ingredients:
                    score += 1

            if score > 0:
                scored_results.append((recipe["name"], score))

        scored_results.sort(key=lambda x: x[1], reverse=True)

        limit = request.args.get('limit', 10, type=int)

        results = [r[0] for r in scored_results[:limit]]

    return render_template(
        'index.html',
        results=results,
        user_input=user_input
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)