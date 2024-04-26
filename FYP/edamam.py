from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import pymysql
import re
import pdfkit
import requests
import json
import os
import urllib.parse
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
APP_ID = "842e0971"
API_KEY = "575c2eecd037076d359a9796716b4d65"
URL = f'https://api.edamam.com/api/recipes/v2?type=public'

# URL = f'https://api.edamam.com/search?q=${mainIngredient}&app_id=${APP_ID}&app_key=${API_KEY}&diet=${diet}&health=${health}&cuisineType=${cuisineType}&mealType=${mealType}&dishType=${dishType}&calories=${calories1}-${calories2}'

# https://api.edamam.com/search?q=${mainIngredient}&app_id=${APP_ID}&app_key=${API_KEY}&from=0&to=${numberOfRecipe}&calories=591-722&health=alcohol-free&imageSize=${imageSize}
# https://api.edamam.com/api/recipes/v2?type=public&app_id=842e0971&app_key=575c2eecd037076d359a9796716b4d65&diet=balanced&health=keto-friendly&cuisineType=American&cuisineType=Chinese
# https://api.edamam.com/api/recipes/v2?type=public&app_id=842e0971&app_key=575c2eecd037076d359a9796716b4d65&health=Mediterranean&cuisineType=American&cuisineType=Asian&cuisineType=British&cuisineType=Caribbean&cuisineType=Central%20Europe&cuisineType=Chinese&cuisineType=Eastern%20Europe&cuisineType=French&cuisineType=Indian&cuisineType=Italian&cuisineType=Japanese&cuisineType=Kosher&cuisineType=Mediterranean&cuisineType=Mexican&cuisineType=Middle%20Eastern&cuisineType=Nordic&cuisineType=South%20American&cuisineType=South%20East%20Asian&dishType=Biscuits%20and%20cookies&dishType=Bread&dishType=Cereals&dishType=Condiments%20and%20sauces&dishType=Desserts&dishType=Drinks&dishType=Main%20course&dishType=Pancake&dishType=Preps&dishType=Preserve&dishType=Salad&dishType=Sandwiches&dishType=Side%20dish&dishType=Soup&dishType=Starter&dishType=Sweets
hits_data = None

@app.route('/')
def recipe():
    return render_template('recipeSearch.html')

@app.route('/search', methods=['POST'])
def search():
    global hits_data
    mainIngredient = request.form.getlist('IngredientsCheck')
    calories1 = request.form['calories1']
    calories2 = request.form['calories2']
    diet = request.form.getlist('DietsCheck')
    health = request.form.getlist('HealthCheck')
    mealType = request.form.getlist('MealtypeCheck')
    dishType = request.form.getlist('DishtypeCheck')
    cuisineType = request.form.getlist('CuisinetypeCheck')

    # Construct the query string with the ingredients
    query = ''
    otherquery = ''
    if 'IngredientsCheck' in request.form:
        for i in mainIngredient:
            encoded_cuisine = i.replace(" ", "%20")
            query += f'&q={encoded_cuisine}'

    if 'DietsCheck' in request.form:
        for i in diet:
            otherquery += f'&diet={i}'
            
    if 'HealthCheck' in request.form:
        for i in health:
            otherquery += f'&health={i}'

    if 'MealtypeCheck' in request.form:
        for i in mealType:
            otherquery += f'&mealType={i}'

    if 'DishtypeCheck' in request.form:
        for i in dishType:
            encoded_cuisine = i.replace(" ", "%20")
            otherquery += f'&dishType={encoded_cuisine}'
                
    if 'CuisinetypeCheck' in request.form:
        for i in cuisineType:
            encoded_cuisine = i.replace(" ", "%20")
            otherquery += f'&cuisineType={encoded_cuisine}'

    url = f'{URL}{query}&app_id={APP_ID}&app_key={API_KEY}&from=0&to=20{otherquery}&calories={calories1}-{calories2}'
    finalurl = url
    print(finalurl)

    # Make a GET request to the Edamam API
    response = requests.get(finalurl)
    response_content = response.text  # Extract the response content as a string
    data = json.loads(response_content)  # Parse the JSON string
    # data = response.json()

    hits = data['hits']
    hits_data = hits
    # return render_template('recipeResult.html', hits=hits)
    return redirect(url_for('recipeOutput'))
    
    recipes = []
    # if 'hits' in data:
    #     for hit in data['hits']:
    #         recipe = hit['recipe']
    #         recipes.append({
    #             'label': recipe['label'],
    #             'image': recipe['image'],
    #             'url': recipe['url'],
    #             'calories': recipe['calories']
    #         })

    # return redirect(url_for('result', recipes=recipes))

@app.route('/recipeOutput')
def recipeOutput():
    global hits_data
    hits = hits_data
    return render_template('recipeResult.html', hits=hits)

@app.route('/error')
def searchError():
    return render_template('recipeError.html')


if __name__=="__main__":
    app.debug = True
    app.run(host="0.0.0.0", port = 5000)