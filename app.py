from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'

db = SQLAlchemy(app)

class Recipe(db.Model):
    __tablename__ = 'recipes' 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/recipe/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        cooking_time = int(request.form['cooking_time'])
        calories = int(request.form['calories'])

        recipe = Recipe(title=title, ingredients=ingredients, cooking_time=cooking_time, calories=calories)
        db.session.add(recipe)
        db.session.commit()

        return redirect('/')
    return render_template('add_recipe.html')

@app.route('/recipe/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.ingredients = request.form['ingredients']
        recipe.cooking_time = int(request.form['cooking_time'])
        recipe.calories = int(request.form['calories'])

        db.session.commit()

        return redirect('/recipe/{}'.format(recipe_id))
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipe/delete/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()

    return redirect('/')
@app.route('/recipe/search', methods=['GET', 'POST'])
def search_recipe():
    if request.method == 'POST':
        search = request.form['search']
        recipe = Recipe.query.filter_by(title=search).first()
        return render_template('recipe.html', recipe=recipe)
    return render_template('search_recipe.html')
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search_term', '')

        # Perform a case-insensitive search on title and ingredients
        results = Recipe.query.filter(
            or_(Recipe.title.ilike(f'%{search_term}%'), Recipe.ingredients.ilike(f'%{search_term}%'))
        ).all()

        return render_template('search_results.html', results=results, search_term=search_term)

    return render_template('search.html')

@app.route('/recipe/search')
def search_page():
    return render_template('search.html')
                                    


if __name__ == '__main__':
    app.run(debug=True)
