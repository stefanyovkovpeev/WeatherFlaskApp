from flask import Flask, redirect, url_for, render_template, request
from App import App

function = App()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/randomcities", methods=["GET", "POST"])
def randomcities():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "generate":
            function.random_cities_generator()
            function.get_weather(function.cities)
            cities_data = function.get_weather_data()
            return render_template("randomcities.html", cities=cities_data)
        elif action == "refresh":
            function.get_weather(function.cities)
            cities_data = function.get_weather_data()
            return render_template("randomcities.html", cities=cities_data)
    elif request.method == "GET":
        cities_data = function.get_weather_data()
        return render_template("randomcities.html", cities=cities_data)

@app.route("/searchedcity", methods=["GET", "POST"])
def search_city():
    if request.method == "POST":
        search_query = request.form.get("search_query")
        cities_data = function.search_city(search_query)
        return render_template("searchedcity.html", city_info = cities_data)
    else:
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()



