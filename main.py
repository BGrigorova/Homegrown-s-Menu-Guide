# import framework for handling the webpage architecture
from flask import Flask, render_template, request, redirect, url_for
# import module for handling csv data
import csv
# create a blank app
app = Flask(__name__)


def load_menu():
    """ Load data from a csv file and build a lowercase dictionary"""
    menu = {}
    with open('menu_items.csv', newline='') as csvfile:
        # convert the csv to dictionary
        reader = csv.DictReader(csvfile)
        for row in reader:
            # make all rows lowercase
            menu[row['Item'].lower()] = row
        # return dictionary
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


if __name__ == "__main__":
    app.run(debug=True)
