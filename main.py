from flask import Flask, render_template, request, redirect, url_for
import requests
import csv
app = Flask(__name__)


def load_menu():
    """ Load data from a csv file and build a lowercase dictionary"""
    menu = {}
    with open('menu_items.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            menu[row['Item'].lower()] = row
        return menu


# assign the menu dictionary to menu_data
menu_data = load_menu()


# home page setup
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry = request.form["menu_item"]
        item = entry.strip().lower()
        if item in menu_data:
            return redirect(url_for("categories", item=item))
        else:
            return redirect(url_for("error"))
    return render_template("home.html")


# categories page setup
@app.route("/categories/<item>")
def categories(item):
    return render_template("categories.html", item=item)


# error page setup
@app.route("/error")
def error():
    return render_template("error.html")


# nutrition macros page setup
@app.route('/nutrition_macros/<item>')
def nutrition_macros(item):
    # Call the microservice running on port 5001
    response = requests.get(f'http://127.0.0.1:5001/nutrition?menu_item_name={item}')
    data = response.json()
    return render_template('nutrition_macros.html', item=item, macros=data)


# allergens page setup
@app.route('/allergens/<item>')
def allergens(item):
    response = requests.get(f'http://127.0.0.1:5002/allergens?menu_item_name={item}')
    data = response.json()
    return render_template('allergens.html', item=item, allergens=data.get('allergens', []))


# calories page setup
@app.route('/calories/<item>')
def calories(item):
    response = requests.get(f'http://127.0.0.1:5003/calories?menu_item_name={item}')
    data = response.json()
    return render_template('calories.html', item=item, calories=data.get('calories', []))


# modifications page setup
@app.route('/modifications/<item>')
def modifications(item):
    response = requests.get(f'http://127.0.0.1:5004/modifications?menu_item_name={item}')
    data = response.json()
    return render_template('modifications.html', item=item, modifications=data.get('modifications', []))


if __name__ == "__main__":
    app.run(debug=True)
