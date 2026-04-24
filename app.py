from flask import Flask, render_template, request

app = Flask(__name__)

recipes = [
    {"name": "Chicken Soup", "ingredients": "chicken water salt"},
    {"name": "Pasta", "ingredients": "pasta tomato cheese"},
    {"name": "Salad", "ingredients": "tomato cucumber lettuce"},
    {"name": "Omelette", "ingredients": "egg milk salt"},
]

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []

    if request.method == 'POST':
        user_input = request.form['ingredients'].lower()

        for recipe in recipes:
            if user_input in recipe["ingredients"]:
                results.append(recipe["name"])

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)