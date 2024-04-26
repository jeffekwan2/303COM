from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import pymysql
import re
import pdfkit
import requests
import json
import os
from fileinput import filename

app = Flask(__name__)
app.secret_key = 'tuesmignonne'

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

connection = pymysql.connect(host = 'localhost', 
    user = 'root',
    password = 'JKHKJEFFmysql115', 
    db = '303com_user', 
    local_infile = 1,
    cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

# IDS = {-1}
URL = 'https://api.edamam.com/search'
APP_ID = "842e0971"
API_KEY = "575c2eecd037076d359a9796716b4d65"
# URL = f'https://api.edamam.com/search?q=${mainIngredient}&app_id=${APP_ID}&app_key=${API_KEY}&diet=${diet}&health=${health}&cuisineType=${cuisineType}&mealType=${mealType}&dishType=${dishType}&calories=${calories1}-${calories2}'

# https://api.edamam.com/search?q=${mainIngredient}&app_id=${APP_ID}&app_key=${API_KEY}&from=0&to=${numberOfRecipe}&calories=591-722&health=alcohol-free&imageSize=${imageSize}
# https://api.edamam.com/api/recipes/v2?type=public&app_id=842e0971&app_key=575c2eecd037076d359a9796716b4d65&diet=balanced&health=keto-friendly&cuisineType=American&cuisineType=Chinese
# https://api.edamam.com/api/recipes/v2?type=public&app_id=842e0971&app_key=575c2eecd037076d359a9796716b4d65&health=Mediterranean&cuisineType=American&cuisineType=Asian&cuisineType=British&cuisineType=Caribbean&cuisineType=Central%20Europe&cuisineType=Chinese&cuisineType=Eastern%20Europe&cuisineType=French&cuisineType=Indian&cuisineType=Italian&cuisineType=Japanese&cuisineType=Kosher&cuisineType=Mediterranean&cuisineType=Mexican&cuisineType=Middle%20Eastern&cuisineType=Nordic&cuisineType=South%20American&cuisineType=South%20East%20Asian&dishType=Biscuits%20and%20cookies&dishType=Bread&dishType=Cereals&dishType=Condiments%20and%20sauces&dishType=Desserts&dishType=Drinks&dishType=Main%20course&dishType=Pancake&dishType=Preps&dishType=Preserve&dishType=Salad&dishType=Sandwiches&dishType=Side%20dish&dishType=Soup&dishType=Starter&dishType=Sweets

@app.route('/')
def recipe():
    return render_template('recipeSearch.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    mainIngredient = request.form.getlist('IngredientsCheck')
    print(mainIngredient)
    calories1 = request.form['calories1']
    calories2 = request.form['calories2']
    diet = request.form.getlist('DietsCheck')
    health = request.form.getlist('HealthCheck')
    mealType = request.form.getlist('MealtypeCheck')
    dishType = request.form.getlist('DishtypeCheck')
    cuisineType = request.form.getlist('CuisinetypeCheck')

    if request.method == 'POST':
        url = constructURL(mainIngredient, calories1, calories2, diet, health, mealType, dishType, cuisineType)
        print(url)

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        recipes = []
        if 'hits' in data:
            for hit in data['hits']:
                recipe = hit['recipe']
                recipes.append({
                    'label': recipe['label'],
                    'image': recipe['image'],
                    'url': recipe['url'],
                    'calories': recipe['calories']
                })

        return redirect(url_for('result', recipes=recipes))

        # except requests.exceptions.HTTPError as e:
        #     error_message = f'Error occurred while accessing the API: {e}'
        #     return render_template('recipeError.html', error_message=error_message)

    return redirect(url_for('recipe'))

def constructURL(mainIngredient, calories1, calories2, diet, health, mealType, dishType, cuisineType):
    params = {
        'app_id': APP_ID,
        'app_key': API_KEY
    }

    if mainIngredient:
        params['q'] = ' '.join(mainIngredient)

    if calories1 and calories2:
        params['calories'] = f'{calories1}-{calories2}'

    if diet:
        params['diet'] = ','.join(diet)

    if health:
        params['health'] = ','.join(health)

    if mealType:
        params['mealType'] = ','.join(mealType)

    if dishType:
        params['dishType'] = ','.join(dishType)

    if cuisineType:
        params['cuisineType'] = ','.join(cuisineType)

    return f'{URL}?{"&".join([f"{k}={v}" for k, v in params.items()])}'

# @app.route('/search', methods =['GET', 'POST'])
# def search():
#     # Get the user's query from the form
#     mainIngredient = request.form.getlist('IngredientsCheck')
#     print(mainIngredient)
#     calories1 = request.form['calories1']
#     calories2 = request.form['calories2']
#     diet = request.form.getlist('DietsCheck')
#     health = request.form.getlist('HealthCheck')
#     mealType = request.form.getlist('MealtypeCheck')
#     dishType = request.form.getlist('DishtypeCheck')
#     cuisineType = request.form.getlist('CuisinetypeCheck')

#     if request.method == 'POST':
#         if 'IngredientsCheck' in request.form:
#             queryMainIngredient(URL, mainIngredient)
#             # print(URL)            

#         if 'calories1' in request.form and 'calories2' in request.form:
#             queryCalories(URL, calories1, calories2)
#             # print(URL)

#         if 'DietsCheck' in request.form:
#             queryDiet(URL, diet)
#             # print(URL)

#         if 'HealthCheck' in request.form:
#             queryHealth(URL, health)
#             # print(URL)

#         if 'MealtypeCheck' in request.form:
#             queryMealType(URL, mealType)
#             # print(URL)

#         if 'DishtypeCheck' in request.form:
#             queryDishType(URL, dishType)
#             # print(URL)

#         if 'CuisinetypeCheck' in request.form:
#             queryCuisineType(URL, cuisineType)
#             # print(URL)
        
#         response = requests.get(URL)
#         data = response.json()

#         data1 = json.loads(data)

#         # Extract the recipe information from the API response
#         recipes = []
#         if 'hits' in data1:
#             for hit in data1['hits']:
#                 recipe = hit['recipe']
#                 recipes.append({
#                     'label': recipe['label'],
#                     'image': recipe['image'],
#                     'url': recipe['url'],
#                     'calories': recipe['calories']
#                 })

#         return redirect(url_for('result', recipes=recipes))

#     # except requests.exceptions.HTTPError as e:
#     #     error_message = f'Error occurred while accessing the API: {e}'
#     #     return render_template('recipeError.html', error_message=error_message)
        

# # multiple if statement to add these to url, need to finish making cards on recipesearch
# # Error handling for each number, 400, 200, 404, etc
# def queryMainIngredient(URL, mainIngredient):
#     for item in mainIngredient:
#         URL = URL + f'&q=${item}'
#     return URL

# def queryCalories(URL, calories1, calories2):
#     URL = URL + f'&calories=${calories1}-${calories2}'
#     return URL

# def queryDiet(URL, diet):
#     for item in diet:
#         URL = URL + f'&diet=${item}'
#     return URL

# def queryHealth(URL, health):
#     for item in health:
#         URL = URL + f'&health=${item}'
#     return URL

# def queryMealType(URL, mealType):
#     for item in mealType:
#         URL = URL + f'&mealType=${item}'
#     return URL

# def queryDishType(URL, dishType):
#     for item in dishType:
#         URL = URL + f'&dishType=${item}'
#     return URL

# def queryCuisineType(URL, cuisineType):
#     for item in cuisineType:
#         URL = URL + f'&cuisineType=${item}'
#     return URL

# def queryRecipeURI(URL, uri):
#     URL =  URL + f'&r={uri}'
#     return URL

@app.route('/result')
def result():
    return render_template('recipeResult.html')

@app.route('/error')
def searchError():
    return render_template('recipeError.html')

if __name__=="__main__":
    app.debug = True
    app.run(host="0.0.0.0", port = 5000)

