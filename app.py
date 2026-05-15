from flask import Flask, render_template, request

app = Flask(__name__)

import pandas as pd

df = pd.read_csv('clean_recipes.csv')

recipes = []

for i in range(len(df)):
    recipes.append({
        "name": df.loc[i, 'clean_title'],
        "ingredients": df.loc[i, 'clean_ingredients']
    })

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []

    if request.method == 'POST':
        user_input = request.form['ingredients'].lower()
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

        # сортировка
        scored_results.sort(key=lambda x: x[1], reverse=True)

        # pagination
        page = request.args.get('page', 1, type=int)

        per_page = request.args.get('limit', 10, type=int)
        start = (page - 1) * per_page
        end = start + per_page

        # только названия
        results = [r[0] for r in scored_results[start:end]]

    else:
        page = 1

    return render_template('index.html', results=results, page=page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)