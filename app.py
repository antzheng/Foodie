from flask import Flask, render_template, request, redirect, url_for
from User import User
import requests
import random

from bs4 import BeautifulSoup

app = Flask(__name__)

user = breakfasts = mainCourses = snacks = locateQuery = None

apiKey = "spoonacular-api-key"

def grabURL(query):
    query = query.replace(" ", "+").replace("+", "%2B").replace("#", "%23").replace("/", "%2F").replace(",", "%2C")
    page = requests.get("https://www.google.com/search?q="+query+"&safe=active&sxsrf=ACYBGNTRcBgqNSZLtwlbkRPjpcefbJHYHA:1572139884843&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiP4P26pbvlAhVjc98KHSKbAbgQ_AUIEigB&biw=1440&bih=765#imgrc=5PIpuh1mN7nmlM")
    soup = BeautifulSoup(page.text, "html.parser")
    listOfLinks = list(soup.find_all("img"))
    num = 1 if len(listOfLinks) >= 2 else 0
    try:
        return (str(listOfLinks[num]).split("src=")[1].split("width")[0])[1:-1]
    except:
        return None

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    global user
    sexes = {'m', 'M', 'f', 'F', 'Female', 'female', 'Male', 'male'}
    males = {'m', 'M', 'Male', 'male'}
    error = None

    if request.method == 'POST':
        try:
            bodyweight = float(request.form['bodyweight'])
            height = float(request.form['height'])
            age = float(request.form['age'])
            if request.form['sex'] not in sexes:
                raise Exception
            sex = 'M' if request.form['sex'] in males else 'F'
            user = User(bodyweight, height, age, sex, float(request.form['activityLevel']))
            return redirect(url_for('main'))
        except:
            error = "Please enter valid information!"

    return render_template("welcome.html", user = user, error = error)

@app.route('/main', methods=['GET', 'POST'])
def main():
    global user, apiKey, breakfasts, mainCourses, snacks, locateQuery

    if request.method == "POST":
        locateQuery = request.form['food']
        return redirect(url_for('locate'))

    if not breakfasts and not mainCourses and not snacks:
        breakfastURL = "https://api.spoonacular.com/food/menuItems/search?query=breakfast&minCalories={}&number=100&apiKey={}".format(user.caloriesNeeded / 3, apiKey)
        mainCourseURL = "https://api.spoonacular.com/food/menuItems/search?query=main%20course&minCalories={}&number=100&apiKey={}".format(user.caloriesNeeded / 3, apiKey)
        snackURL = "https://api.spoonacular.com/food/menuItems/search?query=snack&minCalories={}&number=100&apiKey={}".format(user.caloriesNeeded / 20, apiKey)
        r = requests.get(breakfastURL)
        breakfasts = r.json()['menuItems']
        r = requests.get(mainCourseURL)
        mainCourses = r.json()['menuItems']
        r = requests.get(snackURL)
        snacks = r.json()['menuItems']

    num1, num2, num3, num4 = random.randrange(100), random.randrange(100), random.randrange(100), random.randrange(100)

    while num2 == num3:
        num3 = random.randrange(100)

    breakfastFood = breakfasts[num1]
    lunchFood = mainCourses[num2]
    dinnerFood = mainCourses[num3]
    snackFood = snacks[num4]
    foods = [   (breakfastFood, grabURL(breakfastFood['title'])),
                (lunchFood, grabURL(lunchFood['title'])),
                (dinnerFood, grabURL(dinnerFood['title'])),
                (snackFood, grabURL(snackFood['title']))    ]

    for tup in foods:
        if None in tup:
            return redirect(url_for("main"))

    return render_template("main.html", foods = foods, user = user)

@app.route('/locate', methods=['GET', 'POST'])
def locate():
    global locateQuery
    query = locateQuery.replace(" ", "+").replace("+", "%2B").replace("#", "%23").replace("/", "%2F").replace(",", "%2C")
    return render_template("locate.html", query = query, location = locateQuery)

if __name__ == '__main__':
    app.run(debug=False)
