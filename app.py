from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


#set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsdata_app")


@app.route("/")
def index():
    data = mongo.db.marsfacts.find_one()
    return render_template("index.html", mars_data=data)

@app.route("/scrape")
def scraper():
    marsfacts = mongo.db.marsfacts
    mars_data = scrape_mars.scrape()
    marsfacts.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
